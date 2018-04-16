from __future__ import print_function, division

import sys
import os
import os.path as op
from array import array
from operator import itemgetter
import math

import ROOT
from ROOT import TH1D, TCanvas, gROOT, gPad, TGraph, TGraphErrors, TGraphAsymmErrors, TMultiGraph, TFile, TRandom

gROOT.SetBatch(True)


root_file_old = TFile.Open("data/mjj_data15_13TeV_00276262_physics_Main_total_final.root")
hist_old = root_file_old.Get("mjj_data15_13TeV_00276262_physics_Main_total_final")

root_file_new = TFile.Open("data/mjj_data_new.root")
hist_new = root_file_new.Get("mjj_data17_13TeV_00325713_physics_Main_total_final")

hist_cmp = TH1D(hist_new)

n_bins = hist_old.GetNbinsX()
for b in range(1, n_bins+1):
    data_old = hist_old.GetBinContent(b)
    data_new = hist_new.GetBinContent(b)

    err_old = hist_old.GetBinError(b)
    err_new = hist_new.GetBinError(b)
    if data_new == 0 or data_old == 0:
        continue

    data_cmp = data_new/data_old
    err_cmp = (data_new/data_old)*math.sqrt((err_old/data_old)**2 + (err_new/data_new)**2)

    hist_cmp.SetBinContent(b, data_cmp)
    hist_cmp.SetBinError(b, err_cmp)

#canvas = TCanvas("new/old data", "new/old data", 640, 550)
canvas = TCanvas("new/old data", "new/old data", 420, 380)
canvas.SetBottomMargin(0.15)
canvas.SetLeftMargin(0.15)
canvas.SetTopMargin(0.05)
canvas.SetRightMargin(0.05)
canvas.SetLogx(True)

hist_cmp.GetYaxis().SetTitle("2017/2016 data bin ratio")
hist_cmp.GetYaxis().SetRangeUser(0.9, 1.25)
hist_cmp.GetXaxis().SetRangeUser(1, 4)
hist_cmp.GetXaxis().SetMoreLogLabels(True)
#hist_cmp.SetTitle("New/Old Data")
hist_cmp.SetTitle("")
hist_cmp.Draw("E")

canvas.SaveAs("data_cmp_2.png")
canvas.SaveAs("data_cmp_2.pdf")
