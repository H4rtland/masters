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

void FitExample8(){
  gROOT->Reset();
  
  // This is a comment
  
  // I open the file of interest.
  
  TFile *hfile = new TFile("Test_Fitting_8.root","old","Exercise 1");
  
  // Copy the histogram into memory
  
  TH1F *h_test_1 = (TH1F*)hfile->Get("h_test_1");
  
  // Create a window to plot the rsults of the fit in
  
  TCanvas *TestCanvas = new TCanvas ("TestCanvas","Fitting Test 4",0,0,1200,800);
  
  // fit the histogram with a constant, i.e. a polynomila of degree 1
  
  // Note that this is not a good fit as the distribution is not just gaussian.
  
  h_test_1->Fit("pol1","same");
  
  
  
  // play around with plotting options to allow out put of results
  
  gStyle->SetStatW(0.15);
  gStyle->SetStatH(0.125); 
  gStyle->SetStatColor(5); 
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1111);
  
  // Label x and y axes.
  h_test_1->GetXaxis()->SetTitle("Bin");
  h_test_1->GetYaxis()->SetTitle("Events");
  
  // Set maximum and minimum values of histogram
  //h_test_1->SetMaximum(110.);
  //h_test_1->SetMinimum(50.);
  h_test_1->SetLineWidth(2);
  //h_test_1->Draw();
  h_test_1->Draw("e1");
  TestCanvas->Update();
  
  // Print out histogram 
  
  TestCanvas->Print("Fit_Example_8.ps");
  TestCanvas->Print("Fit_Example_8.gif");
  
  
  // Get fit parameters into variables
  TF1 *fit = h_test_1->GetFunction("pol1");
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
  
  char *s = new char[1];
  cout << endl << " Hit <enter> to continue" << endl;
  gets(s);
  
  
  // Now we will fit with a function + Gaussian
  
  
  // define a new function, gaussian + constant 
  TF1 *my_func = new TF1("my_func","gaus+([3]+x*[4])",0,50);
  

  
  // set the initail values of the function to the fit values plus a constant of 50. 
  
  // Need to guess Gaussian location etc. I assume centered at 50., with width 5 and 100 norm
  my_func->SetParameters(100.,50.,5.,p[0],p[1]);
  // draw it to see how it looks 
  my_func->SetLineColor(2);
  
  my_func->Draw("same");
  
  
  s = new char[1];
  cout << endl << " Hit <enter> to continue" << endl;
  gets(s);
  
  
  cout << " Now fitting with seperate function " << endl << endl; 
  h_test_1->Fit("my_func","same");
  h_test_1->Draw("e1");
  
  
  TestCanvas->Print("Fit_Example_8_new.pdf");
  TestCanvas->Print("Fit_Example_8_new.gif");
  
  
  // Get fit parameters into variables
  TF1 *new_fit = h_test_1->GetFunction("my_func");
   chi2 = new_fit->GetChisquare();
  Double_t p_n[5];
  new_fit->GetParameters(p_n);
  
  Double_t e_n[5];
  for(Int_t i=0; i<5; i++){
    e_n[i] = new_fit->GetParError(i);
  }
  
      ndf = new_fit->GetNDF();
  cout << endl << endl;
  cout << " Output of Fit Parameters " << endl;
  cout << " ======================== " << endl << endl;   
  
  cout << " The chi^2 = " << chi2 << " for " << ndf << " degrees of freedom " << endl;
  
  cout << " The gaussian fitted constant value = " << p_n[0] << " +/- " << e_n[0] << endl;
  cout << " The fitted mean              value = " << p_n[1] << " +/- " << e_n[1] << endl;
  cout << " The fitted sigma             value = " << p_n[2] << " +/- " << e_n[2] << endl;
  cout << " The fitted constant          value = " << p_n[3] << " +/- " << e_n[3] << endl;
  cout << " The fitted slope             value = " << p_n[4] << " +/- " << e_n[4] << endl;
  
  
  
}

