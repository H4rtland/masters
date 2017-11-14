#include "Functions.h"


Double_t background(Double_t *x, Double_t *par){
  return par[0] +par[1]*x[0];
}

Double_t GausPeak(Double_t *x, Double_t *par){
  Double_t arg=0.;
  if (par[2]) arg = (x[0] - par[1])/par[2];
  Double_t func_val = par[0]*TMath::Exp(-0.5*arg*arg);
  return func_val;
}

Double_t CombFunc(Double_t *x, Double_t *par){
  return background(x,par) + GausPeak(x,&par[2]);
}
