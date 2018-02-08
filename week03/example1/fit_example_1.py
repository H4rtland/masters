from ROOT import TFile, TH1D, TCanvas, gStyle, gROOT

# Don't open a window to show the canvas       
# Only want to save it to an image file
gROOT.SetBatch(True)

def fit_example():
    root_file = TFile.Open("Test_Fitting_1.root")
    
    h_test_1 = root_file.Get("h_test_1")
    
    test_canvas = TCanvas("TestCanvas", "Fitting Test", 0, 0, 650, 450)
    
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
    
    test_canvas.SaveAs("Fit_Example_1.pdf")
    test_canvas.SaveAs("Fit_Example_1.png")
    
    fit = h_test_1.GetFunction("pol0")
    
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
