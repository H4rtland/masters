from ROOT import TFile, TH1D, TCanvas, gStyle

def fit_example():
    root_file = TFile.Open("Test_Fitting_1.root")
    
    h_test_1 = root_file.Get("h_test_1")
    
    test_canvas = TCanvas("TestCanvas", "Fitting Test", 0, 0, 600, 400)
    
    h_test_1.Fit("pol0", "same")
    
    gStyle.SetStatW(0.15)
    gStyle.SetStatH(0.125)
    gStyle.SetStatColor(5)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(1111)
    
    h_test_1.GetXaxis().SetTitle("Bin")
    h_test_1.GetYaxis().SetTitle("Events")
    
    h_test_1.SetMaximum(130)
    h_test_1.SetMinimum(30)
    h_test_1.SetLineWidth(2)
    # Somehow drawing the canvas ruins the style in the printed pdf
    #h_test_1.Draw("e1")
    #raw_input()
    
    test_canvas.Update()
    test_canvas.Print("Fit_Example_1.pdf")
    test_canvas.Print("Fit_Example_1.png")
    
    fit = h_test_1.GetFunction("pol0")
    #fit.SetLineColor(2)
    #fit.SetLineWidth(2)
    #fit.Draw("same")
    #test_canvas.Update()
    #raw_input()
    
    chi2 = fit.GetChisquare()
    p1 = fit.GetParameter(0)
    e1 = fit.GetParError(0)
    ndf = fit.GetNDF()
    print ""
    print " Output of fit parameters "
    print " ======================== "
    print " The chi^2 = {0} for {1} degrees of freedom".format(chi2, ndf)
    print " The fitted constant value = {0} +/- {1}".format(p1, e1)
    
fit_example()
