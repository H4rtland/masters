from __future__ import print_function
import math
import os.path as op
import operator
from scipy.stats import poisson
import random
import time
import sys

from array import array
import ROOT
from ROOT import TFile, TH1D, TCanvas, gStyle, gROOT, TF1, TColor, TMinuit, gPad, TPad
from ROOT import TGaxis, TBox, THStack, TLegend, TGraphErrors, TVectorD, TGraph
from ROOT.Math import GaussIntegrator, WrappedTF1, IParamFunction
from ROOT.Math import IParametricFunctionOneDim

gROOT.SetBatch(True)


class BackgroundModel:
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def model_at(self, x):
        scale = x/14
        a1 = self.p1 * math.pow(1-scale, self.p2)
        a2 = self.p3 + (self.p4 * math.log(scale))
        a3 = math.pow(scale, a2)
        return a1*a3

    def random_at(self, x):
        return poisson.ppf(random.random(), self.model_at(x))


class Fits:
    def __init__(self):
        
        self.p_n = [0,]*100
        self.e_n = [0,]*100
        self.stored_parameters = [0,]*100
        
        self.num_bins = 0
        self.xmins = []
        self.xmaxes = []
        
        self.data = []
        self.errors = []
        self.data_fits = []

        self.model_scale_values = []
        self.final = False
        
        self.exclude_regions = ((0, 0),)
        
        self.col1 = 1
        self.col2 = TColor.GetColor(27, 158, 119)
        self.col3 = TColor.GetColor(217, 95, 2)
        self.col4 = TColor.GetColor(117, 112, 179)
        
    def run_mass_fit(self, peak_scale_initial):
        self.gMinuit = TMinuit(30)
        self.gMinuit.SetPrintLevel(-1)
        self.gMinuit.SetFCN(self.Fitfcn_max_likelihood)
        
        arglist = array("d", [0,]*10)
        ierflg = ROOT.Long(0)
        arglist[0] = ROOT.Double(1)
        
        # peak_scale_initial = ROOT.Double(peak_scale_initial)

        tmp = array("d", [0,])
        self.gMinuit.mnexcm("SET NOWarnings", tmp, 0, ierflg); 

        self.gMinuit.mnexcm("SET ERR", arglist, 1, ierflg)
        self.gMinuit.mnparm(0, "p1", 5e-6, 1e-7, 0, 0, ierflg)
        self.gMinuit.mnparm(1, "p2", 10, 10, 0, 0, ierflg)
        self.gMinuit.mnparm(2, "p3", -5.3, 1, 0, 0, ierflg)
        self.gMinuit.mnparm(3, "p4", -4e-2, 1e-2, 0, 0, ierflg)
        self.gMinuit.mnparm(4, "p5", peak_scale_initial, peak_scale_initial/50, 0, 0, ierflg)
        
        
        self.background_fit_only = [0,]*len(self.data)

        arglist[0] = ROOT.Double(0)
        arglist[1] = ROOT.Double(0)

        self.exclude_regions = ((2.2, 3.3),)
        self.gMinuit.FixParameter(2)
        self.gMinuit.FixParameter(3)
        self.gMinuit.FixParameter(4)
        
        self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
        self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)
        
        self.gMinuit.Release(2)
        self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
        self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)
        
        self.gMinuit.Release(3)
        self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
        self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)

        # Find an actual best fit
        self.exclude_regions = ((0, 2), (3.3, 100),)
        self.gMinuit.FixParameter(0)
        self.gMinuit.FixParameter(1)
        self.gMinuit.FixParameter(2)
        self.gMinuit.FixParameter(3)
        self.gMinuit.Release(4)
        self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
        self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)

        self.exclude_regions = ()
        self.gMinuit.Release(0)
        self.gMinuit.Release(1)
        self.gMinuit.Release(2)
        self.gMinuit.Release(3)
        self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
        self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)

        best_fit_value = ROOT.Double(0)
        self.gMinuit.mnstat(best_fit_value, ROOT.Double(0), ROOT.Double(0),
                            ROOT.Long(0), ROOT.Long(0), ROOT.Long(0))
        #print("Best fit value", best_fit_value)

        # And prepare for iterating over fit values for N injected events
        self.gMinuit.Release(0)
        self.gMinuit.Release(1)
        self.gMinuit.Release(2)
        self.gMinuit.Release(3)
        self.exclude_regions = ()

        #self.data_fits = no_peak_data_fits
        x_values = []
        y_values = []

        fitted_N = ROOT.Double(0)
        self.gMinuit.GetParameter(4, fitted_N, ROOT.Double(0))
        best_fit_likelihood = self.calc_likelihood(fitted_N)

        for N in range(0, 2501, 10):
            fit_likelihood = self.calc_likelihood(N)
            x_values.append(N)
            y_values.append(fit_likelihood-best_fit_likelihood)

        return x_values, y_values
    

    def Fitfcn_max_likelihood(self, npar, gin, fcnVal, par, iflag):
        likelihood = 0
        mf = ROOT.MyMassSpectrum()
        mf.SetParameters(par)
        ig = GaussIntegrator()
        ig.SetFunction(mf)
        ig.SetRelTolerance(0.00001)
        
        for i in range(0, self.num_bins):
            for lower, higher in self.exclude_regions:
                if lower < self.xmins[i] < higher:
                    continue

            model_val = ig.Integral(self.xmins[i], self.xmaxes[i]) / (self.xmaxes[i]-self.xmins[i])
            self.background_fit_only[i] = model_val
            model_val += self.model_scale_values[i]*par[4]
            self.data_fits[i] = model_val

            likelihood += model_val - self.data[i]
            if self.data[i] > 0 and model_val > 0:
                likelihood += self.data[i]*(math.log(self.data[i])-math.log(model_val))
        
        fcnVal[0] = likelihood


    def calc_likelihood(self, peak_scale):
        like = 0

        for i in range(0, self.num_bins):
            if self.data_fits[i] <= 0:
                continue

            p = peak_scale*self.model_scale_values[i]
            tmp = ROOT.TMath.PoissonI(self.data[i], self.background_fit_only[i]+p)
            #if peak_scale == 40000:
            #    print(i, "\txmin", self.xmins[i], "\tdata", self.data[i], "\tdata_fit", self.data_fits[i], "\tp", p, "\tdata_fit+p", self.data_fits[i]+p)
            if tmp == 0:
                print("tmp == 0 here")
                logtmp = math.log(sys.float_info.min)
            else:
                logtmp = math.log(tmp)
            like += logtmp

        return -like




def fit_significance(num_injected_events, plot=True):

    # pre-fitted background parameters to generate random distributions from
    background = BackgroundModel(1.70475e1, 8.43990, -4.63149, -2.43023e-3)

    ROOT.IABstyles.global_style()
    TGaxis.SetMaxDigits(3)

    root_file = TFile.Open("data15_13TeV_background.root")
    hist = root_file.Get("mjj_data15_13TeV_00276262_physics_Main_total_final")
    
    root_file_qstar = TFile.Open("dataLikeHistograms.QStar3000.root")
    nominal = root_file_qstar.GetDirectory("Nominal")
    hist_model = nominal.Get("mjj_Scaled_QStar3000_30fb")
    hist_model.Smooth(1)
    hist_model.Scale(1/hist_model.Integral())
    model_scale_values = [hist_model.GetBinContent(b) for b in range(1, hist_model.GetNbinsX()+1)]
    hist_model.Scale(num_injected_events)
    total_peak = 0

    for b in range(1, hist.GetNbinsX()+1):
        if hist.GetBinContent(b) > 0 or hist.GetBinLowEdge(b)/1000 > 2:
            x = hist.GetBinCenter(b)/1000
            bg = background.random_at(x)
            peak = 0
            if hist_model.GetBinContent(b) > 0:
                peak = poisson.ppf(random.random(), hist_model.GetBinContent(b))
            total_peak += peak
            hist.SetBinContent(b, bg+peak)
    
    fits = Fits()
    fits.model_scale_values = model_scale_values 

    nbins = hist.GetNbinsX()
    xwidth = [(hist.GetBinLowEdge(b+1)/1000-hist.GetBinLowEdge(b)/1000)/2 for b in range(1, nbins+1)]
    xmiddle = [hist.GetBinCenter(b)/1000 for b in range(1, nbins+1)]
        
    fits.xmins = [hist.GetBinLowEdge(b)/1000 for b in range(1, nbins+1)]
    fits.xmaxes = [hist.GetBinLowEdge(b+1)/1000 for b in range(1, nbins+1)]
    fits.data = [hist.GetBinContent(b) for b in range(1, nbins+1)]
    fits.data_fits = [0,]*nbins
    
    fits.errors = [math.sqrt(x) for x in fits.data]
    fits.num_bins = nbins
    
    
    remove_bins = 0
    for x in fits.data:
        if x == 0:
            remove_bins += 1
        else:
            break
    
    nbins -= remove_bins
    xwidth = xwidth[remove_bins:]
    xmiddle = xmiddle[remove_bins:]
    fits.xmins = fits.xmins[remove_bins:]
    fits.xmaxes = fits.xmaxes[remove_bins:]
    fits.data = fits.data[remove_bins:]
    fits.data_fits = fits.data_fits[remove_bins:]
    fits.errors = fits.errors[remove_bins:]
    fits.num_bins = nbins
    fits.model_scale_values = fits.model_scale_values[remove_bins:]

    x, y = fits.run_mass_fit(num_injected_events)
    y = [math.exp(-a) for a in y]
    
    ycumulative = [sum(y[0:i]) for i in range(0, len(y))]
    ycumulative = [yval/max(ycumulative) for yval in ycumulative]
    limit_x = 0
    limit_y = 0
    for xv, yv in zip(x, ycumulative):
        if yv >= 0.95:
            limit_x = xv
            limit_y = yv
            break
    
    if not plot:
        return limit_x
    
    canvas = TCanvas("dist", "dist", 0, 0, 650, 450)
    graph = TGraph(len(x), array("d", x), array("d", y))
    ROOT.IABstyles.h1_style(graph, ROOT.IABstyles.lWidth/2, ROOT.IABstyles.Scolor, 1, 0, 0, -1111.0, -1111.0, 508, 508, 8, ROOT.IABstyles.Scolor, 0.1, 0)
    graph.SetMarkerColor(2)
    graph.SetMarkerStyle(3)
    graph.SetMarkerSize(1.25)
    graph.Draw("ap")
    canvas.SaveAs("sig_dist.png")

    canvas2 = TCanvas("cumsum", "cumsum", 0, 0, 650, 450)
    graph = TGraph(len(x), array("d", x), array("d", ycumulative))
    ROOT.IABstyles.h1_style(graph, ROOT.IABstyles.lWidth/2, ROOT.IABstyles.Scolor, 1, 0, 0, -1111.0, -1111.0, 508, 508, 8, ROOT.IABstyles.Scolor, 0.1, 0)
    graph.SetMarkerColor(4)
    graph.SetMarkerStyle(3)
    graph.SetMarkerSize(1.25)
    graph.Draw("ap")
    line = ROOT.TLine(limit_x, 0, limit_x, limit_y)
    line.SetLineColor(2)
    line.Draw("same")
    label = ROOT.TText()
    label.SetNDC()
    label.SetTextSize(0.03)
    label.DrawText(0.5, 0.7, "{0:.02f} confidence limit = {1} events".format(limit_y, limit_x))
    canvas2.SaveAs("sig_cumsum.png")

def plot_95pc_confidence_dist():
    gROOT.LoadMacro("FitFunction.cpp+g")
    gROOT.LoadMacro("IABStyle.cpp+g")

    """canvas = TCanvas("dist", "dist", 0, 0, 650, 450)
    hist = TH1D("dist", "95% C.L dist", 100, 0, 1500)
    for i in range(0, 300):
        if i %25 == 0:
            print(i)
        hist.Fill(fit_significance(0, plot=False))
    hist.Draw()
    canvas.SaveAs("95pcCL_dist.png")"""
    
    start_time = time.time()
    
    with open("results/job-{0}.txt".format(sys.argv[1]), "w") as out_file:
        for i in range(0, 250):
            out_file.write("{0}\n".format(fit_significance(0, plot=False)))
    
    print("Took {0:.02} seconds".format(time.time()-start_time))

plot_95pc_confidence_dist()
    
