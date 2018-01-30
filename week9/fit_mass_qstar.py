import math
import os.path as op
import operator
from scipy.stats import poisson
import random
import time

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

        self.gMinuit.Release(0)
        self.gMinuit.Release(1)
        self.gMinuit.Release(2)
        self.gMinuit.Release(3)
        self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
        self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)

        best_fit_value = ROOT.Double(0)
        self.gMinuit.mnstat(best_fit_value, ROOT.Double(0), ROOT.Double(0),
                            ROOT.Long(0), ROOT.Long(0), ROOT.Long(0))

        # And prepare for iterating over fit values for N injected events
        self.gMinuit.Release(0)
        self.gMinuit.Release(1)
        self.gMinuit.Release(2)
        self.gMinuit.Release(3)
        self.exclude_regions = ()

        x_values = []
        y_values = []

        for N in range(36000, 44001, 200):
            self.gMinuit.DefineParameter(4, "p5", N, 0, 0, 1e12)
            self.gMinuit.FixParameter(4)
            self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
            self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)
            fit_value = ROOT.Double(0)
            self.gMinuit.mnstat(fit_value, ROOT.Double(0), ROOT.Double(0),
                                ROOT.Long(0), ROOT.Long(0), ROOT.Long(0))
            x_values.append(N)
            y_values.append(fit_value-best_fit_value)

        return x_values, y_values
    
    def Fitfcn(self, npar, gin, fcnVal, par, iflag):
        chisq = 0
        mf = ROOT.MyMassSpectrum()
        mf.SetParameters(par)
        ig = GaussIntegrator()
        ig.SetFunction(mf)
        ig.SetRelTolerance(0.00001)
        
        for i in range(0, self.num_bins):
            val = ig.Integral(self.xmins[i], self.xmaxes[i])/(self.xmaxes[i]-self.xmins[i])
            chiValue = 0
            if self.errors[i]:
                chiValue = (self.data[i]-val)/math.sqrt(val)
            chiValue *= chiValue
            chisq += chiValue
            self.data_fits[i] = val
        
        fcnVal[0] = chisq

    def Fitfcn_max_likelihood(self, npar, gin, fcnVal, par, iflag):
        likelihood = 0
        mf = ROOT.MyMassSpectrum()
        mf.SetParameters(par)
        ig = GaussIntegrator()
        ig.SetFunction(mf)
        ig.SetRelTolerance(0.00001)
        
        model_total = 0

        events_total = 0
        
        for i in range(0, self.num_bins):
            for lower, higher in self.exclude_regions:
                if lower < self.xmins[i] < higher:
                    continue
            
            model_val = ig.Integral(self.xmins[i], self.xmaxes[i]) / (self.xmaxes[i]-self.xmins[i])
            #if self.final:
            #    print(self.xmins[i], model_val, self.model_scale_values[i]*par[4])
            model_val += self.model_scale_values[i]*par[4]
            
            self.data_fits[i] = model_val
            
            
            if model_val <= 0 or (self.data[i] == 0 and self.xmins[i] < 2):
                continue

            likelihood += self.data[i] * math.log(model_val)

            model_total += model_val
            events_total += self.data[i]

        
        fcnVal[0] = 2*(model_total-likelihood)


def fit_mass():
    # pre-fitted background parameters to generate random distributions from
    background = BackgroundModel(1.70475e1, 8.43990, -4.63149, -2.43023e-3)

    gROOT.LoadMacro("IABStyle.cpp+g")
    ROOT.IABstyles.global_style()
    TGaxis.SetMaxDigits(3)

    root_file = TFile.Open("data15_13TeV_background.root")
    hist = root_file.Get("mjj_data15_13TeV_00276262_physics_Main_total_final")
    
    root_file_blackmax = TFile.Open("dataLikeHistograms.QStar3000.root")
    nominal = root_file_blackmax.GetDirectory("Nominal")
    hist_model = nominal.Get("mjj_Scaled_QStar3000_30fb")
    hist_model.Smooth(1)
    hist_model.Scale(1/hist_model.Integral())
    hist_model.Scale(40000)
    # Model data started one bin earlier than actual data
    # so there was a lone low value right at the start
    # of the data+model which was dragging the fit down.
    # This removes that.
    #for b in range(1, hist.GetNbinsX()+1):
    #   if hist.GetBinContent(b) == 0:
    #       hist_model.SetBinContent(b, 0)
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
    print("Total peak:, ", total_peak)
    fits = Fits()
    fits.model_scale_values = [hist_model.GetBinContent(b) for b in range(1, hist_model.GetNbinsX()+1)]

    #hist_model.Scale(2)
    #hist.Add(hist_model)
    
    nbins = hist.GetNbinsX()
    xwidth = [(hist.GetBinLowEdge(b+1)/1000-hist.GetBinLowEdge(b)/1000)/2 for b in range(1, nbins+1)]
    xmiddle = [hist.GetBinCenter(b)/1000 for b in range(1, nbins+1)]
        
        
    fits.xmins = [hist.GetBinLowEdge(b)/1000 for b in range(1, nbins+1)]
    fits.xmaxes = [hist.GetBinLowEdge(b+1)/1000 for b in range(1, nbins+1)]
    fits.data = [hist.GetBinContent(b) for b in range(1, nbins+1)]
    fits.data_fits = [0,]*nbins
    
    fits.errors = [math.sqrt(x) for x in fits.data]
    fits.num_bins = nbins

    fits.run_mass_fit(1.0)
    
    test_canvas = TCanvas("TestCanvas", "Ds Fit", 0, 0, 800, 575)

    gStyle.SetPadBorderMode(0)
    gStyle.SetFrameBorderMode(0)

    test_canvas.Divide(1, 2, 0, 0)
    upper_pad = test_canvas.GetPad(1)#TPad("upper_pad", "upper_pad", 0.005, 0.7525, 0.995, 0.995)
    lower_pad = test_canvas.GetPad(2)#TPad("lower_pad", "lower_pad", 0.005, 0.005,  0.995, 0.7475)
    low, high = 0.05, 0.95
    upper_pad.SetPad(low, 0.4, high, high)
    lower_pad.SetPad(low, low, high, 0.4)
    
    test_canvas.cd(1)
    
    ROOT.IABstyles.canvas_style(test_canvas, 0.25, 0.05, 0.02, 0.15, 0, 0)
    
    h_Mjj = TH1D("h_Mjj", "Mass Spectrum", 100, 0.2, 12)
    h_Mjj.GetYaxis().SetTitle("num. events")
    h_Mjj.GetXaxis().SetTitle("M [Tev/c^{-2}]")
    
    ROOT.IABstyles.h1_style(h_Mjj, ROOT.IABstyles.lWidth/2, ROOT.IABstyles.Scolor, 1, 0, 0, -1111.0, -1111.0, 508, 508, 8, ROOT.IABstyles.Scolor, 0.1, 0)
    
    h_Mjj.GetYaxis().SetRangeUser(0.1, 1e6)
    h_Mjj.GetXaxis().SetRangeUser(1, 10)
    h_Mjj.GetXaxis().SetTitleOffset(1)
    h_Mjj.GetYaxis().SetTitleOffset(1.1)
    
    upper_pad.SetLogy(1)
    upper_pad.SetLogx(1)
    lower_pad.SetLogx(1)
    
    gr = TGraphErrors(fits.num_bins, array("d", xmiddle), array("d", fits.data), array("d", xwidth), array("d", fits.errors))
    ROOT.IABstyles.h1_style(gr, ROOT.IABstyles.lWidth/2, ROOT.IABstyles.Scolor, 1, 0, 0, -1111, -1111, 505, 505, 8, ROOT.IABstyles.Scolor, 0.1, 0)
    
    grFit = TGraph(fits.num_bins, array("d", xmiddle), array("d", fits.data_fits))
    ROOT.IABstyles.h1_style(grFit, ROOT.IABstyles.lWidth/2, 632, 1, 0, 0, -1111, -1111, 505, 505, 8, 632, 0.1, 0)
    
    h_Mjj.Draw("axis")
    gr.Draw("P")
    grFit.Draw("c")
    #upper_pad.Draw()

    def gaus(x, par):
        arg = 0
        if par[2] != 0:
            arg = (x[0] - par[1]) / par[2]
        return par[0] * math.exp(-0.5*arg*arg)

    gauss_f = TF1("gauss_f", gaus, 1000, 2900, 100)
    gauss_f.SetParameters(1000, 2900, 100)
    gauss_f.SetLineColor(3)
    gauss_f.Draw("same")

    test_canvas.Update()
    
    gPad.SetBottomMargin(1e-5)
    
    test_canvas.cd(2)
    gPad.SetTopMargin(1e-5)
    
    """h2 = TH1D("h2", "Significance", fits.num_bins, 0.2, 12)
    h2.GetYaxis().SetTitle("Significance")
    for bin_num, (data, theory) in enumerate(zip(fits.data, fits.data_fits), start=1):
        print("bin", bin_num, data, theory, (data-theory)/theory)
        h2.SetBinContent(bin_num, (data-theory)/theory)
    h2.GetXaxis().SetRangeUser(1, 10)
        
    h2.Draw()"""
    h2 = TH1D("h2", "", 100, 0.2, 12)
    h2.GetXaxis().SetRangeUser(1, 10)
    h2.GetYaxis().SetRangeUser(-10, 10)
    h2.SetStats(False) # don't show stats box
    h2.Draw("axis")
    sig_values = [(data-theory)/theory if data!= 0 else -100 for data, theory in zip(fits.data, fits.data_fits)]
    sig = TGraph(fits.num_bins, array("d", xmiddle), array("d", sig_values))
    #ROOT.IABstyles.h1_style(sig, ROOT.IABstyles.lWidth/2, 632, 1, 0, 0, -1111, -1111, 505, 505, 8, 632, 0.1, 0)
    ROOT.IABstyles.h1_style(gr, ROOT.IABstyles.lWidth/2, ROOT.IABstyles.Scolor, 1, 0, 0, -1111, -1111, 505, 505, 8, ROOT.IABstyles.Scolor, 0.1, 0)
    sig.SetMarkerStyle(22) # triangle
    sig.SetMarkerColor(2)  # red
    sig.SetMarkerSize(0.8)
    sig.Draw("P")
    #lower_pad.Draw()
    
    # test_canvas.SaveAs("output_qstar.pdf")
    test_canvas.SaveAs("output_qstar.png")



def fit_peak(num_injected_events):
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
    hist_model.Scale(num_injected_events)
    # Model data started one bin earlier than actual data
    # so there was a lone low value right at the start
    # of the data+model which was dragging the fit down.
    # This removes that.
    #for b in range(1, hist.GetNbinsX()+1):
    #   if hist.GetBinContent(b) == 0:
    #       hist_model.SetBinContent(b, 0)
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
    fits.model_scale_values = [hist_model.GetBinContent(b) for b in range(1, hist_model.GetNbinsX()+1)]

    nbins = hist.GetNbinsX()
    xwidth = [(hist.GetBinLowEdge(b+1)/1000-hist.GetBinLowEdge(b)/1000)/2 for b in range(1, nbins+1)]
    xmiddle = [hist.GetBinCenter(b)/1000 for b in range(1, nbins+1)]
        
    fits.xmins = [hist.GetBinLowEdge(b)/1000 for b in range(1, nbins+1)]
    fits.xmaxes = [hist.GetBinLowEdge(b+1)/1000 for b in range(1, nbins+1)]
    fits.data = [hist.GetBinContent(b) for b in range(1, nbins+1)]
    fits.data_fits = [0,]*nbins
    
    fits.errors = [math.sqrt(x) for x in fits.data]
    fits.num_bins = nbins

    fits.run_mass_fit(1.0)

    par4 = ROOT.Double(0)
    par4_error = ROOT.Double(0)

    fits.gMinuit.GetParameter(4, par4, par4_error)

    hist_model.Scale(par4)
    return hist_model.Integral()

def fit_many():
    start_time = time.time()
    gROOT.LoadMacro("FitFunction.cpp+g")
    gROOT.LoadMacro("IABStyle.cpp+g")
    distribution = TH1D("dist", "dist", 60, 37000, 43000)
    with open("results.txt", "w") as out_file:
        for i in range(0, 200):
            if i%10 == 0:
                print("Starting trial {0}".format(i))
            n = fit_peak(40000)
            out_file.write("{0}\n".format(n))
            distribution.Fill(n)

    canvas = TCanvas("Canvas", "Distribution Canvas", 0, 0, 650, 450)
    distribution.Draw()
    canvas.SaveAs("dist.png")

    print("Took {0:.2f} seconds in total".format(time.time()-start_time))

# fit_many()





def fit_significance(num_injected_events):
    gROOT.LoadMacro("FitFunction.cpp+g")
    gROOT.LoadMacro("IABStyle.cpp+g")

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
    fits.model_scale_values = [hist_model.GetBinContent(b)/num_injected_events for b in range(1, hist_model.GetNbinsX()+1)]

    nbins = hist.GetNbinsX()
    xwidth = [(hist.GetBinLowEdge(b+1)/1000-hist.GetBinLowEdge(b)/1000)/2 for b in range(1, nbins+1)]
    xmiddle = [hist.GetBinCenter(b)/1000 for b in range(1, nbins+1)]
        
    fits.xmins = [hist.GetBinLowEdge(b)/1000 for b in range(1, nbins+1)]
    fits.xmaxes = [hist.GetBinLowEdge(b+1)/1000 for b in range(1, nbins+1)]
    fits.data = [hist.GetBinContent(b) for b in range(1, nbins+1)]
    fits.data_fits = [0,]*nbins
    
    fits.errors = [math.sqrt(x) for x in fits.data]
    fits.num_bins = nbins

    x, y = fits.run_mass_fit(num_injected_events)
    y = [1/a for a in y]
    #print(list(zip(x, y)))
    #par4 = ROOT.Double(0)
    #par4_error = ROOT.Double(0)

    #fits.gMinuit.GetParameter(4, par4, par4_error)
   
    canvas = TCanvas("dist", "dist", 0, 0, 650, 450)
    graph = TGraph(len(x), array("d", x), array("d", y))
    ROOT.IABstyles.h1_style(graph, ROOT.IABstyles.lWidth/2, ROOT.IABstyles.Scolor, 1, 0, 0, -1111.0, -1111.0, 508, 508, 8, ROOT.IABstyles.Scolor, 0.1, 0)
    graph.SetMarkerColor(2)
    graph.SetMarkerStyle(3)
    graph.SetMarkerSize(1.5)
    graph.Draw("ap")
    canvas.SaveAs("sig_dist.png")

fit_significance(40000)
