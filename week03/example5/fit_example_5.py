from ROOT import TFile, TH1D, TCanvas, gStyle, gROOT

gROOT.SetBatch(True)

def fit_example_5():
    root_file = TFile.Open("Test_Fitting_5.root")
    
    h_test_1 = root_file.Get("h_test_1")
    
    test_canvas = TCanvas("TestCanvas", "Fitting Test 5", 0, 0, 650, 450)
    
    h_test_1.Fit("gaus", "same")
    
    gStyle.SetStatW(0.15)
    gStyle.SetStatH(0.125)
    gStyle.SetStatColor(5)
    gStyle.SetOptStat(5)
    gStyle.SetOptFit(1111)
    
    h_test_1.GetXaxis().SetTitle("Bin")
    h_test_1.GetYaxis().SetTitle("Events")
    
    h_test_1.SetLineWidth(2)
    
    test_canvas.SaveAs("Fit_Example_5.png")
    
    fit = h_test_1.GetFunction("gaus")

    chi2 = fit.GetChisquare()

    parameters = fit.GetParameters()
    errors = [fit.GetParError(i) for i in range(0, 3)]

    ndf = fit.GetNDF()

    print " Output of Fit Parameters "
    print " ======================== "
    print " The chi^2 = {0} for {1} degrees of freedom".format(chi2, ndf)
    print " The fitted constant value = {0} +/- {1}".format(parameters[0], errors[0])
    print " The fitted mean     value = {0} +/- {1}".format(parameters[1], errors[1])
    print " The fitted sigma    value = {0} +/- {1}".format(parameters[2], errors[2])    

fit_example_5()
