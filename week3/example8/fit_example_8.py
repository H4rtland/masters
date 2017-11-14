from ROOT import TFile, TH1D, TCanvas, gStyle, gROOT, TF1

gROOT.SetBatch(True)

def fit_example_8():
    root_file = TFile.Open("Test_Fitting_8.root")
    
    h_test_1 = root_file.Get("h_test_1")
    
    test_canvas = TCanvas("TestCanvas", "Fitting Test 8", 0, 0, 650, 450)
    
    h_test_1.Fit("pol1", "same")
    
    gStyle.SetStatW(0.15)
    gStyle.SetStatH(0.125)
    gStyle.SetStatColor(5)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(1111)

    h_test_1.GetXaxis().SetTitle("Bin")
    h_test_1.GetYaxis().SetTitle("Events")
    
    h_test_1.SetLineWidth(2)
    
    test_canvas.SaveAs("Fit_Example_8.png")
    
    fit = h_test_1.GetFunction("pol1")
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
    
    # Now fit function + gaussian
    
    my_func = TF1("my_func", "gaus+([3]+x*[4])", 0, 50)
    my_func.SetParameters(100, 50, 5, p[0], p[1])
    my_func.SetLineColor(2)
    
    h_test_1.Fit("my_func", "same")
    
    test_canvas.SaveAs("Fit_Example_8_2.png")
    
    new_fit = h_test_1.GetFunction("my_func")
    chi2 = new_fit.GetChisquare()
    p = new_fit.GetParameters()
    e = [new_fit.GetParError(i) for i in range(0, 5)]
    ndf = new_fit.GetNDF()

    print "\n"
    print " Output of New Fit Parameters "
    print " ======================== "
    print " The chi^2 = {0} for {1} degrees of freedom".format(chi2, ndf)
    print " The gaussian fitted constant value = {0} +/- {1}".format(p[0], e[0])
    print " The fitted mean              value = {0} +/- {1}".format(p[1], e[1])
    print " The fitted sigma             value = {0} +/- {1}".format(p[2], e[2])
    print " The fitted constant          value = {0} +/- {1}".format(p[3], e[3])
    print " The fitted slope             value = {0} +/- {1}".format(p[4], e[4])
    
fit_example_8()
