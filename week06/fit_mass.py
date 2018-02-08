import math
import os.path as op
import operator

from array import array
import ROOT
from ROOT import TFile, TH1D, TCanvas, gStyle, gROOT, TF1, TColor, TMinuit
from ROOT import TGaxis, TBox, THStack, TLegend, TGraphErrors, TVectorD, TGraph
from ROOT.Math import GaussIntegrator, WrappedTF1, IParamFunction
from ROOT.Math import IParametricFunctionOneDim

gROOT.SetBatch(True)

class MyMassSpectrum(IParametricFunctionOneDim):
    def __init__(self):
        self.pars = None
    
    def Clone(self):
        return MyMassSpectrum()
    
    def DoEval(self, x):
        scale = x/14
        arg1 = self.pars[0]*math.pow(1-scale, self.pars[1])
        arg2 = self.pars[2]+self.pars[3]*math.log(scale)
        arg3 = math.pow(scale, arg2)
        return arg1*arg3
    
    def DoEvalPar(self, x, p):
        scale = x/14
        arg1 = self.pars[0]*math.pow(1-scale, self.pars[1])
        arg2 = self.pars[2]+self.pars[3]*math.log(scale)
        arg3 = math.pow(scale, arg2)
        return arg1*arg3
        
    def Parameters(self):
        return self.pars
    
    def SetParameters(self, p):
        self.pars = p
        
    def NPar(self):
        return 4



class Fits:
    def __init__(self):
        gROOT.LoadMacro("FitFunction.cpp+g")
        
        self.p_n = [0,]*100
        self.e_n = [0,]*100
        self.stored_parameters = [0,]*100
        
        self.num_bins = 0
        self.xmins = []
        self.xmaxes = []
        
        self.data = []
        self.errors = []
        self.data_fits = []
        
        self.col1 = 1
        self.col2 = TColor.GetColor(27, 158, 119)
        self.col3 = TColor.GetColor(217, 95, 2)
        self.col4 = TColor.GetColor(117, 112, 179)
        
    def run_mass_fit(self):
        self.gMinuit = TMinuit(30)
        self.gMinuit.SetFCN(self.Fitfcn_max_likelihood)
        
        arglist = array("d", [0,]*10)
        ierflg = ROOT.Long(0)
        arglist[0] = ROOT.Double(1)
        
        self.gMinuit.mnexcm("SET ERR", arglist, 1, ierflg)
        self.gMinuit.mnparm(0, "p1", 5e-6, 1e-7, 0, 0, ierflg)
        self.gMinuit.mnparm(1, "p2", 10, 10, 0, 0, ierflg)
        self.gMinuit.mnparm(2, "p3", -5.3, 1, 0, 0, ierflg)
        self.gMinuit.mnparm(3, "p4", -4e-2, 1e-2, 0, 0, ierflg)
        
        arglist[0] = ROOT.Double(0)
        arglist[1] = ROOT.Double(0)
        
        self.gMinuit.FixParameter(2)
        self.gMinuit.FixParameter(3)
        
        self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
        self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)
        
        self.gMinuit.Release(2)
        self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
        self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)
        
        self.gMinuit.Release(3)
        self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
        self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)

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
            model_val = ig.Integral(self.xmins[i], self.xmaxes[i]) / (self.xmaxes[i]-self.xmins[i])
            self.data_fits[i] = model_val
            if model_val <= 0 or (self.data[i] == 0 and self.xmins[i] < 2):
                continue

            likelihood += self.data[i] * math.log(model_val)

            model_total += model_val
            events_total += self.data[i]

        
        fcnVal[0] = 2.*(model_total-likelihood)


def fit_mass():
    gROOT.LoadMacro("IABStyle.cpp+g")
    ROOT.IABstyles.global_style()
    TGaxis.SetMaxDigits(3)

    root_file = TFile.Open("mjj_data15_13TeV_00276262_physics_Main_total_final.root")
    hist = root_file.Get("mjj_data15_13TeV_00276262_physics_Main_total_final")
    
    nbins = hist.GetNbinsX()
    xwidth = [(hist.GetBinLowEdge(b+1)/1000-hist.GetBinLowEdge(b)/1000)/2 for b in range(1, nbins+1)]
    xmiddle = [hist.GetBinCenter(b)/1000 for b in range(1, nbins+1)]
        
        
    fits = Fits()
    fits.xmins = [hist.GetBinLowEdge(b)/1000 for b in range(1, nbins+1)]
    fits.xmaxes = [hist.GetBinLowEdge(b+1)/1000 for b in range(1, nbins+1)]
    fits.data = [hist.GetBinContent(b) for b in range(1, nbins+1)]
    fits.data_fits = [0,]*nbins
    
    fits.errors = [math.sqrt(x) for x in fits.data]
    fits.num_bins = nbins
    
    fits.run_mass_fit()
    
    test_canvas = TCanvas("TestCanvas", "Ds Fit", 0, 0, 800, 575)
    
    ROOT.IABstyles.canvas_style(test_canvas, 0.25, 0.05, 0.02, 0.15, 0, 0)
    
    h_Mjj = TH1D("h_Mjj", "Mass Spectrum", 100, 0.2, 12)
    h_Mjj.GetYaxis().SetTitle("num. events")
    h_Mjj.GetXaxis().SetTitle("M [Tev/c^{-2}]")
    
    ROOT.IABstyles.h1_style(h_Mjj, ROOT.IABstyles.lWidth/2, ROOT.IABstyles.Scolor, 1, 0, 0, -1111, -1111, 508, 508, 8, ROOT.IABstyles.Scolor, 0.1, 0)
    
    h_Mjj.GetYaxis().SetRangeUser(0.1, 1e6)
    h_Mjj.GetXaxis().SetRangeUser(1, 10)
    h_Mjj.GetXaxis().SetTitleOffset(1)
    h_Mjj.GetYaxis().SetTitleOffset(1.1)
    
    test_canvas.SetLogy(1)
    test_canvas.SetLogx(1)
    
    gr = TGraphErrors(fits.num_bins, array("d", xmiddle), array("d", fits.data), array("d", xwidth), array("d", fits.errors))
    ROOT.IABstyles.h1_style(gr, ROOT.IABstyles.lWidth/2, ROOT.IABstyles.Scolor, 1, 0, 0, -1111, -1111, 505, 505, 8, ROOT.IABstyles.Scolor, 0.1, 0)
    
    grFit = TGraph(fits.num_bins, array("d", xmiddle), array("d", fits.data_fits))
    ROOT.IABstyles.h1_style(grFit, ROOT.IABstyles.lWidth/2, 632, 1, 0, 0, -1111, -1111, 505, 505, 8, 632, 0.1, 0)
    
    h_Mjj.Draw("axis")
    gr.Draw("P")
    grFit.Draw("c")
    test_canvas.Update()
    
    test_canvas.SaveAs("log_likelihood_output.pdf")
    test_canvas.SaveAs("log_likelihood_output.png")

fit_mass()
