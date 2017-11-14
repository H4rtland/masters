#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <sstream>
#include <string>
#include <iostream>
#include <iomanip>
#include <fstream>

#include "TMath.h"
#include "TFile.h"
#include "TTree.h"
#include "TBrowser.h"
#include "TH1.h"
#include "TH2.h"
#include "TROOT.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TF1.h"
#include "Functions.h"

void FitExample10(){
  gROOT->Reset();
  
  // This is a comment
  
  // I am going to load a library of functions
  
  gROOT->LoadMacro("Functions.C+g");
  
  // I open the file of interest.
  
  TFile *hfile = new TFile("Test_Fitting_10.root","old","Exercise 1");
  
  // Copy the histogram into memory
  
  TH1F *h_test_1 = (TH1F*)hfile->Get("h_test_1");
  
  // Create a window to plot the rsults of the fit in
  
  TCanvas *TestCanvas = new TCanvas ("TestCanvas","Fitting Test 10",0,0,1200,800);
  
  // We now want to crate a root function based on one of the library functions that 
  // I ave created in the file Functions.C
  
  
  // the background will be over the range 0.->200., with two parameters
  
  TF1 *backgnd = new TF1("backgnd",background,0,200.,2);
  
  // The signal will also be over the range 0.->200., with 3 parameters
  
  TF1 *GPeak  = new TF1("GPeak",GausPeak,0,200.,3);
  
  // fit to the background
  
  h_test_1->Fit("backgnd");
  h_test_1->Draw("e1, same");
  
  // get out the parameters 
  
  // Get fit parameters into variables
  TF1 *fit = h_test_1->GetFunction("backgnd");
  Double_t chi2 = fit->GetChisquare();
  Double_t p[2];
  fit->GetParameters(p);
  Double_t e[2];
  for(Int_t i=0; i<2; i++){
    e[i] = fit->GetParError(i);
  }
  
  Int_t    ndf = fit->GetNDF();
  cout << endl << endl;
  cout << " Output of Fit Parameters " << endl;
  cout << " ======================== " << endl << endl;   
  
  cout << " The chi^2 = " << chi2 << " for " << ndf << " degrees of freedom " << endl;
  
  cout << " The fitted constant value = " << p[0] << " +/- " << e[0] << endl;
  cout << " The fitted slope    value = " << p[1] << " +/- " << e[1] << endl;
  
  
  
  TestCanvas->Update();
  
  
  TF1 *comb = new TF1("comb",CombFunc,0,200.,5);
  
  
  
  char *s = new char[1];
  cout << endl << " Hit <enter> to continue" << endl;
  gets(s);
  
  //Try again by setting some initial parameters
  
  comb->SetParameter(0,p[0]);
  comb->SetParameter(1,p[1]);
  
  // set Gaussian initial parameters
  
  
  comb->SetParameter(2,1000.); // Normalization
  comb->SetParameter(3,50.); // Mean = 50.
  comb->SetParameter(4,5.); // width = 5.

  gPad->SetLogy();  

  
  
  h_test_1->Fit("comb","V");
  h_test_1->Draw("e1");
  
  
  
  TestCanvas->Update();
  
  
  
   chi2 = comb->GetChisquare();
  Double_t p_n[5];
  comb->GetParameters(p_n);
  
  Double_t e_n[5];
  for(Int_t i=0; i<5; i++){
    e_n[i] = comb->GetParError(i);
  }
  
      ndf = comb->GetNDF();
  cout << endl << endl;
  cout << " Output of Fit Parameters " << endl;
  cout << " ======================== " << endl << endl;   
  
  cout << " The chi^2 = " << chi2 << " for " << ndf << " degrees of freedom " << endl;
  
  cout << " The fitted constant          value = " << p_n[0] << " +/- " << e_n[0] << endl;
  cout << " The fitted slope             value = " << p_n[1] << " +/- " << e_n[1] << endl;
  cout << endl;
  cout << " The gaussian fitted constant value = " << p_n[2] << " +/- " << e_n[2] << endl;
  cout << " The fitted mean              value = " << p_n[3] << " +/- " << e_n[3] << endl;
  cout << " The fitted sigma             value = " << p_n[4] << " +/- " << e_n[4] << endl;
  
  
  backgnd->SetParameters(p_n);
  backgnd->SetLineColor(2);
  backgnd->Draw("same");
  
  GPeak->SetParameters(&p_n[2]);
  GPeak->SetLineColor(3);
  GPeak->Draw("same");
  
  TestCanvas->Update();
  
  TestCanvas->Print("Fit_Example_10.pdf");
  TestCanvas->Print("Fit_Example_10.gif");
  
  
  
  s = new char[1];
  cout << endl << " Hit <enter> to continue" << endl;
  gets(s);
  
  hfile->Close();
}
