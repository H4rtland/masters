#include <fstream>
#include <iomanip>
#include <iostream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <string>
#include <vector>

#include "IABStyle.h"
//#include "IABFunctions.h"
#include "TDatime.h"

#include "TMinuit.h"
#include "TRandom3.h"

#include "Math/GaussIntegrator.h"
#include "Math/IFunction.h"
#include "Math/IParamFunction.h"
#include "Math/WrappedParamFunction.h"
#include "Math/WrappedTF1.h"
#include "TBox.h"
#include "TGaxis.h"
#include "THStack.h"
#include "TLegend.h"

#include "TGraphErrors.h"
#include "TVectorD.h"

#include "TColor.h"

using std::left;
using std::right;

using namespace std;

// c++ class used for integrating a function in root (yes it is complicated)
class MyMassSpectrum : public ROOT::Math::IParametricFunctionOneDim {
  private:
    const double *pars;

  public:
    // this method is the actual function. In this case x is the mass
    // scale =x/sqrt{s}
    double DoEval(double x) const {

        Double_t scale = x / 14.;
        Double_t arg1 = pars[0] * TMath::Power((1. - scale), pars[1]);
        Double_t arg2 = pars[2] + pars[3] * TMath::Log(scale);
        Double_t arg3 = TMath::Power(scale, arg2);
        return arg1 * arg3;
        // return (x * p[0]) + (x * x * p[1]);
    }

    // implementation that allows you to set and change paramaters
    double DoEvalPar(double x, const double *p) const {

        Double_t scale = x / 14.;
        Double_t arg1 = p[0] * TMath::Power((1. - scale), p[1]);
        Double_t arg2 = p[2] + p[4] * TMath::Log(scale);
        Double_t arg3 = TMath::Power(scale, arg2);
        return arg1 * arg3;
        return (x * p[0]) + (x * x * p[1]);
    }

    ROOT::Math::IBaseFunctionOneDim *Clone() const { return new MyMassSpectrum(); }

    const double *Parameters() const { return pars; }

    void SetParameters(const double *p) { pars = p; }

    unsigned int NPar() const { return 4; }
};

namespace Fits {

TRandom3 *rGen = new TRandom3();

TDatime *now = new TDatime();

TString text;

Double_t p_n[100];
Double_t e_n[100];

Double_t stored_paramaters[100];

TCanvas *TestCanvas;
TFile *hfile;
TFile *of;

// Axes
Int_t Number_Bins;
Double_t xmin[600];
Double_t xmax[600];

// Unweighted data
Double_t Data[600];
Double_t Error[600];
Double_t DataFit[600];

Int_t col1 = 1; // TColor::GetColor( 51,  34, 136);
Int_t col2 = TColor::GetColor(27, 158, 119);
Int_t col3 = TColor::GetColor(217, 95, 2);
Int_t col4 = TColor::GetColor(117, 112, 179);

// Minuit, the fitting package used in root...

TMinuit *gMinuit;
extern void Fitfcn(Int_t &npar, Double_t *grad, Double_t &fcnval, Double_t *xval, Int_t iflag);

// used for names and fitting setup...
Double_t inputParamaters[20];

const string par_name[] = {};

void runMassFit() {

    // setup minuit with a maximum of 30 paramaters
    gMinuit = new TMinuit(30);

    // tells minuit which method to minimise.
    gMinuit->SetFCN(Fitfcn);

    Double_t arglist[10];
    Int_t ierflg = 0;

    arglist[0] = 1;

    // tells minuit to use a chi^2 fit error definition
    gMinuit->mnexcm("SET ERR", arglist, 1, ierflg);

    // definition of paramater names and initial parametrs
    // this is an art.
    gMinuit->mnparm(0, "p1", 5e-6, 1e-7, 0, 0, ierflg);
    gMinuit->mnparm(1, "p2", 10, 10, 0, 0, ierflg);
    gMinuit->mnparm(2, "p3", -5.3, 1, 0, 0, ierflg);
    gMinuit->mnparm(3, "p4", -4e-2, 1e-2, 0, 0, ierflg);

    // Now ready for minimization step - ???
    arglist[0] = 0.;
    arglist[1] = 0.;

    // fix starting paramaters
    gMinuit->FixParameter(2);
    gMinuit->FixParameter(3);

    // run simplex minimisation
    gMinuit->mnexcm("simplex", arglist, 2, ierflg);
    // run migrad
    gMinuit->mnexcm("MIGRAD", arglist, 2, ierflg);

    // release and rerun fits

    gMinuit->Release(2);
    gMinuit->mnexcm("simplex", arglist, 2, ierflg);

    gMinuit->mnexcm("MIGRAD", arglist, 2, ierflg);

    gMinuit->Release(3);
    gMinuit->mnexcm("simplex", arglist, 2, ierflg);

    gMinuit->mnexcm("MIGRAD", arglist, 2, ierflg);
}

void Fitfcn(Int_t &npar, Double_t *gin, Double_t &fcnVal, Double_t *par, Int_t iflag) {

    switch (iflag) {
    default: {

        // define c^2
        Double_t chisq = 0.;

        // define fitting function
        MyMassSpectrum *mf = new MyMassSpectrum();

        mf->SetParameters(par);
        ROOT::Math::GaussIntegrator ig;
        ig.SetFunction(*mf);

        // set size of integral accuracy.
        ig.SetRelTolerance(0.00001);
        for (int i = 0; i < Fits::Number_Bins; i++) {

            // define value as integral from xmin to xmax dividied by bin
            // width which is usual for cross sections. Look
            // up cross section defn.
            double val = ig.Integral(xmin[i], xmax[i]) / (xmax[i] - xmin[i]);
            double chiValue = 0.;

            // caclulate chi^2
            if (Error[i])
                chiValue = (Data[i] - val) / Error[i];

            chiValue *= chiValue;
            chisq += chiValue;

            DataFit[i] = val;
            /**
            if (i==0 || i==10) {
                cout << i << "\t";
                cout << val << "\t";
                cout << Data[i] << "\t";
                cout << chiValue << "\n";
            }
             */
        }

        fcnVal = chisq;
    }
    }
}
}

void FitMass() {

    // Load basic fit fucntions
    // gROOT->LoadMacro("IABFunctions.C+g");
    gROOT->LoadMacro("IABStyle.C+g");

    // set the maximum numbner of digits on axes labels
    IABstyles::global_style();
    TGaxis::SetMaxDigits(3);

    // read in data.
    ifstream inputData;
    inputData.open("xsection.txt");

    double x1, x2, xs1;
    int b1;
    Fits::Number_Bins = 0;

    Double_t xmiddle[1000];
    Double_t xwidth[1000];
    while (inputData >> x1 >> x2 >> b1 >> xs1) {

        // cout << test << endl;
        // read in and convert to TeV.
        Fits::xmin[b1] = x1 / 1000.;

        Fits::xmax[b1] = x2 / 1000.;

        xwidth[b1] = (0.5 * (x2 - x1)) / 1000.;
        xmiddle[b1] = Fits::xmin[b1] + xwidth[b1];

        Fits::Data[b1] = xs1;
        // xwidth[b1] = (0.5*(x2-x1))/1000.;
        // xmiddle[b1] = xmin[b1] + xwidth[b1];
        Fits::Error[b1] = xs1 * 0.05;
        // cout << b1 << "\t" << x1 << "\t" << x2 << "\t" << xs1 << endl;
        Fits::Number_Bins += 1;
    }
    inputData.close();

    // run mass fit..
    Fits::runMassFit();

    // plot results
    TCanvas *TestCanvas;

    TestCanvas = new TCanvas("TestCanvas", "Ds Fit", 0, 0, 1200, 1200);
    IABstyles::canvas_style(TestCanvas, 0.15, 0.05, 0.02, 0.15, 0, 0);

    TH1D *h_Mjj = new TH1D("h_Mjj", "Mass Spectrum", 100, 0.2, 12.);
    h_Mjj->GetYaxis()->SetTitle("d#sigma/dM [pb/GeVc^{ -2}]");
    h_Mjj->GetXaxis()->SetTitle("M [TeV/c^{ 2}]");

    IABstyles::h1_style(h_Mjj, IABstyles::lWidth, IABstyles::Scolor, 1, 0, 0, -1111., -1111., 508, 508, 8, IABstyles::Scolor, 1.2, 0);
    h_Mjj->GetYaxis()->SetRangeUser(1e-12, 1e4);
    h_Mjj->GetXaxis()->SetTitleOffset(1.0);
    h_Mjj->GetYaxis()->SetTitleOffset(1.1);

    TestCanvas->SetLogy(1);
    TestCanvas->SetLogx(1);
    TGraph *gr = new TGraphErrors(Fits::Number_Bins, xmiddle, Fits::Data, xwidth, Fits::Error);
    IABstyles::h1_style(gr, IABstyles::lWidth, IABstyles::Scolor, 1, 0, 0, -1111., -1111., 505, 505, 8, IABstyles::Scolor, 1.2, 0);

    TGraph *grFit = new TGraph(Fits::Number_Bins, xmiddle, Fits::DataFit);
    IABstyles::h1_style(grFit, IABstyles::lWidth, kRed, 1, 0, 0, -1111., -1111., 505, 505, 8, kRed, 1.2, 0);
    // TArrow *arr =  new TArrow(1., xmax-1000., 1., xmax-250., 0.01, ">");
    // arr->SetLineWidth(IABstyles::lWidth);

    h_Mjj->Draw("axis");
    gr->Draw("P");
    grFit->Draw("c");
    // arr->Draw();
    // gr->Print();
    TestCanvas->Update();
    // cout << xmax << endl;

    TestCanvas->Update();
    TestCanvas->Print("Xsection_2014_10_27.pdf");
}