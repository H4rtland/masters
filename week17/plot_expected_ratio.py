from __future__ import print_function, division

import sys
import math
import os
import os.path as op
from array import array
from operator import itemgetter


import ROOT
from ROOT import TH1D, TCanvas, gROOT, gStyle, gPad, TGraph, TGraphErrors, TGraphAsymmErrors, TMultiGraph, TFile, TRandom, TRandom1, TLatex, TLegend

gROOT.SetBatch(True)


def read_data(filename):
    with open(filename, "r") as data_file:
        data = {}
        name = data_file.readline()
        print("Reading ", filename, name)
        for line in data_file.readlines():
            e, m, cs = line.split(":")
            if e == "e":
                m = int(float(m))
                cs = float(cs)
                data[m] = cs
    return data

qs37 = read_data("b_61672.txt")
qs79 = read_data("b_69206.txt")
qbh37 = read_data("b_61673.txt")
qbh79 = read_data("b_69207.txt")
wp37 = read_data("b_61674.txt")
wp79 = read_data("b_69208.txt")


canvas = TCanvas("ratiosabc", "ratiosabc", 0, 0, 530, 450)
canvas.SetBottomMargin(0.125)
canvas.SetLeftMargin(0.135)
canvas.SetTopMargin(0.05)
canvas.SetRightMargin(0.05)


x = array("d", list(sorted(qs37.keys())))
y = array("d", [qs79[m]/qs37[m] for m in sorted(qs37.keys())])
lineqs = TGraph(len(x), x, y)
lineqs.SetLineStyle(1)
lineqs.SetLineColor(1)
lineqs.SetLineWidth(2)
lineqs.SetMarkerStyle(8)
lineqs.SetMarkerSize(0.75)
lineqs.SetMarkerColor(1)
lineqs.Draw("axisPL")

lineqs.GetYaxis().SetRangeUser(0.4, 0.75)
lineqs.GetXaxis().SetRangeUser(1500, 10500)
lineqs.GetXaxis().SetLimits(1500, 10500)
lineqs.GetXaxis().SetNdivisions(506)
lineqs.GetXaxis().SetTitle("m_{jj} [GeV]")
lineqs.GetXaxis().SetTitleSize(0.05)
lineqs.GetYaxis().SetTitleSize(0.05)
lineqs.GetXaxis().SetTitleOffset(1.1)
lineqs.GetYaxis().SetTitleOffset(1.35)
lineqs.GetXaxis().SetLabelSize(0.045)
lineqs.GetYaxis().SetLabelSize(0.045)
lineqs.GetYaxis().SetTitle("79 fb^{-1} #sigma #times A #times BR / 37 fb^{-1} #sigma #times A #times BR")

lineqs.SetTitle("")

lineqs.Draw("axisPL")
canvas.Update()

x = array("d", list(sorted(qbh37.keys())))
y = array("d", [qbh79[m]/qbh37[m] for m in sorted(qbh37.keys())])
lineqbh = TGraph(len(x), x, y)
lineqbh.SetLineStyle(1)
lineqbh.SetLineColor(2)
lineqbh.SetLineWidth(2)
lineqbh.SetMarkerStyle(8)
lineqbh.SetMarkerSize(0.75)
lineqbh.SetMarkerColor(2)
lineqbh.Draw("samePL")


x = array("d", list(sorted(wp37.keys())))
y = array("d", [wp79[m]/wp37[m] for m in sorted(wp37.keys())])
linewp = TGraph(len(x), x, y)
linewp.SetLineStyle(1)
linewp.SetLineColor(3)
linewp.SetLineWidth(2)
linewp.SetMarkerStyle(8)
linewp.SetMarkerSize(0.75)
linewp.SetMarkerColor(3)
linewp.Draw("samePL")

line = ROOT.TLine()
line.SetLineColor(1)
line.SetLineWidth(2)
line.SetLineStyle(9)
_y = math.sqrt(37/79)
line.DrawLine(1500, _y, 10500, _y)


legend = TLegend(0.75+0.04, 0.75-0.2, 0.96+0.04, 0.9-0.2)
legend.SetMargin(0.35)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.AddEntry(lineqs, "q*", "l")
legend.AddEntry(lineqbh, "QBH", "l")
legend.AddEntry(linewp, "W'", "l")
#legend.AddEntry(data_line, "Observed 95% CL upper limit", "lp")
#legend.AddEntry(brazil_line, "Expected 95% CL upper limit", "l")
#legend.AddEntry(brazil_yellow, "Expected #pm1#sigma and #pm2#sigma")
legend.Draw()

canvas.SaveAs("expected_ratios.png")
canvas.SaveAs("expected_ratios.pdf")
