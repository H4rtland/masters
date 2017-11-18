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
        self.pars = []
    
    def Clone(self):
        return MyMassSpectrum()
    
    def DoEval(self, x):
        scale = x/14
        arg1 = pars[0]*math.pow(1-scale, pars[1])
        arg2 = pars[2]+pars[3]*math.log(scale)
        arg3 = math.pow(scale, arg2)
        return arg1*arg3
    
    def DoEvalPar(self, x, p):
        scale = x/14
        arg1 = pars[0]*math.pow(1-scale, pars[1])
        arg2 = pars[2]+pars[3]*math.log(scale)
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
        self.gMinuit.SetFCN(self.Fitfcn)
        
        arglist = array("d", [0,]*10)
        ierflg = ROOT.Long(0)
        arglist[0] = ROOT.Double(1)
        #import pprint
        #pprint.pprint(dir(self.gMinuit))
        #self.gMinuit.mnexcm("SET ERR", arglist, 1, ierflg)
        self.gMinuit.mnparm(0, "p1", 5e-6, 1e-7, 0, 0, ierflg)
        self.gMinuit.mnparm(1, "p2", 10, 10, 0, 0, ierflg)
        self.gMinuit.mnparm(2, "p3", -5.3, 1, 0, 0, ierflg)
        self.gMinuit.mnparm(3, "p4", -4e2, 1e-2, 0, 0, ierflg)
        
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
        print("Doing fitfcn")
        chisq = 0
        mf = MyMassSpectrum()
        mf.SetParameters(par)
        ig = GaussIntegrator()
        ig.SetFunction(mf)
        ig.SetRelTolerance(0.00001)
        
        for i in range(0, self.num_bins):
            val = ig.Integral(self.xmins[i], self.xmaxes[i])/(self.xmaxes[i]-self.xmins[i])
            chiValue = 0
            
            chiValue = (self.data[i]-val)/self.errors[i]
            chisq += chiValue
            self.data_fits[i] = val
        
        fcnVal[0] = chisq


def fit_mass():
    gROOT.LoadMacro("IABStyle.C+g")
    ROOT.IABstyles.global_style()
    TGaxis.SetMaxDigits(3)

    with open("xsection.txt", "r") as input_file:
        data = input_file.readlines()
        data = [d.split() for d in data]
        data = [[float(x_left)/1000, float(x_right)/1000, int(bin_num), float(xs2)]
                    for x_left, x_right, bin_num, xs2 in data]

        xwidth = [x_right-x_left for x_left, x_right, _, _ in data]
        xmiddle = [(x_left+x_right)/2 for x_left, x_right, _, _ in data]
        
    fits = Fits()
    fits.xmins = list(map(operator.itemgetter(0), data))
    fits.xmaxes = list(map(operator.itemgetter(1), data))
    fits.data = list(map(operator.itemgetter(3), data))
    fits.data_fits = [0,]*len(data)
    
    fits.errors = [xs1*0.05 for _, _, _, xs1 in data]
    fits.num_bins = len(data)
    
    fits.run_mass_fit()
    
    test_canvas = TCanvas("TestCanvas", "Ds Fit", 0, 0, 1200, 1200)
    
    ROOT.IABstyles.canvas_style(test_canvas, 0.25, 0.05, 0.02, 0.15, 0, 0)
    
    h_Mjj = TH1D("h_Mjj", "Mass Spectrum", 100, 0.2, 12)
    h_Mjj.GetYaxis().SetTitle("d#sigma/dM [pb/GeVc^{-2}]")
    h_Mjj.GetXaxis().SetTitle("M [Tev/c^{-2}]")
    
    ROOT.IABstyles.h1_style(h_Mjj, ROOT.IABstyles.lWidth, ROOT.IABstyles.Scolor, 1, 0, 0, -1111, -1111, 508, 508, 8, ROOT.IABstyles.Scolor, 1.2, 0)
    
    h_Mjj.GetYaxis().SetRangeUser(1e-12, 1e4)
    h_Mjj.GetXaxis().SetTitleOffset(1)
    h_Mjj.GetYaxis().SetTitleOffset(1.1)
    
    test_canvas.SetLogy(1)
    test_canvas.SetLogx(1)
    
    gr = TGraphErrors(fits.num_bins, array("d", xmiddle), array("d", fits.data), array("d", xwidth), array("d", fits.errors))
    ROOT.IABstyles.h1_style(gr, ROOT.IABstyles.lWidth, ROOT.IABstyles.Scolor, 1, 0, 0, -1111, -1111, 505, 505, 8, ROOT.IABstyles.Scolor, 1.2, 0)
    
    grFit = TGraph(fits.num_bins, array("d", xmiddle), array("d", fits.data_fits))
    ROOT.IABstyles.h1_style(grFit, ROOT.IABstyles.lWidth, 632, 1, 0, 0, -1111, -1111, 505, 505, 8, 632, 1.2, 0)
    
    h_Mjj.Draw("axis")
    gr.Draw("P")
    grFit.Draw("c")
    test_canvas.Update()
    
    test_canvas.SaveAs("output.pdf")

fit_mass()
