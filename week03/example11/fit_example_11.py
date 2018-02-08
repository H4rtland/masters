import math

from ROOT import TFile, TH1D, TCanvas, gStyle, gROOT, gPad, TF1

gROOT.SetBatch(True)

def background(x, par):
    return par[0] + par[1]*x[0]
    
def gaus_peak(x, par):
    arg = 0
    if par[2] != 0:
        arg = (x[0] - par[1]) / par[2]
    func_val = par[0] * math.exp(-0.5*arg*arg)
    return func_val
    
def comb_func(x, par):
    return background(x, par) + gaus_peak(x, (par[2], par[3], par[4]))

def fit_example_11():
    root_file = TFile.Open("Test_Fitting_10.root")

    h_test_1 = root_file.Get("h_test_1")

    test_canvas = TCanvas("TestCanvas", "Fitting Test 10", 0, 0, 650, 450)

    backgnd = TF1("backgnd", background, 0, 200, 2)
    peak = TF1("peak", gaus_peak, 0, 200, 3)
    
    h_test_1.Fit("backgnd")

    test_canvas.Update()
    test_canvas.SaveAs("Fit_Example_11.png")

    fit = h_test_1.GetFunction("backgnd")
    chi2 = fit.GetChisquare()
    p = fit.GetParameters()
    e = [fit.GetParError(i) for i in [0, 1]]
    ndf = fit.GetNDF()

    print "\n"
    print " Output of Fit Parameters "
    print " ======================== "
    print " The chi^2 = {0} for {1} degrees of freedom".format(chi2, ndf)
    print " The fitted constant value = {0} +/- {1}".format(p[0], e[0])
    print " The fitted slope   value = {0} +/- {1}".format(p[1], e[1])
    
    #raw_input("Press enter to continue")
    
    comb = TF1("comb", comb_func, 0, 200, 5)
    
    #h_test_1.Fit("comb")
    #h_test_1.Draw()
    #test_canvas.Update()
        
    comb.SetParameter(0, p[0])
    comb.SetParameter(1, p[1])
    
    comb.SetParameter(2, 0) # normalization
    comb.SetParameter(3, 50) # mean
    #comb.SetParameter(3, 50, 50) # fix mean to 50
    comb.SetParameter(4, 5) # width
    #comb.SetParameter(4, 5, 5) # fix width to 5
    comb.FixParameter(3, 50) # this works to fix parameters
    comb.FixParameter(4, 5)

    h_test_1.Fit("comb")
    h_test_1.Draw("same")
    
    test_canvas.Update()
    
    chi2 = comb.GetChisquare()
    p_n = comb.GetParameters()
    e_n = [comb.GetParError(i) for i in range(0, 5)]
    ndf = comb.GetNDF()
    
    backgnd.SetParameters(p_n)
    backgnd.SetLineColor(2)
    backgnd.Draw("same")
    
    peak.SetParameters(p_n[2], p_n[3], p_n[4])
    peak.SetLineColor(3)
    peak.Draw("same")
    
    test_canvas.SaveAs("Fit_Example_11_2.png")


fit_example_11()
