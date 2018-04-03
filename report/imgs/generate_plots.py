from __future__ import print_function, division

import sys
import math
import os
import os.path as op
from array import array
from operator import itemgetter

import ROOT
from ROOT import TH1D, TCanvas, gROOT, gStyle, gPad, TGraph, TGraphErrors, TGraphAsymmErrors, TMultiGraph, TFile, TRandom, TLatex, TLegend

gROOT.SetBatch(True)
#gROOT.LoadMacro("IABStyle.cpp+g")
#ROOT.IABstyles.global_style()
#gStyle.SetLegendBorderSize(0)
#gStyle.SetLegendFillStyle(0);

canvas = TCanvas("pythia", "pythia", 0, 0, 600, 450)
canvas.SetLogy(True)
canvas.SetBottomMargin(0.11)
canvas.SetLeftMargin(0.11)
canvas.SetTopMargin(0.05)
canvas.SetRightMargin(0.05)
#ROOT.IABstyles.canvas_style(canvas, 0.25, 0.05, 0.02, 0.15, 0, 0)

pythia_file = TFile.Open("Fourth_Year_Data/mjj_mc15_13TeV_361023_Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W_total_final.root")
pythia_hist = pythia_file.Get("mjj_mc15_13TeV_361023_Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W_total_final")

pythia_hist.GetYaxis().SetTitle("Events")
pythia_hist.GetYaxis().SetTitleSize(0.04)
pythia_hist.GetYaxis().SetLabelSize(0.035)
pythia_hist.GetYaxis().SetNdivisions(508)

pythia_hist.GetXaxis().SetTitleSize(0.04)
pythia_hist.GetXaxis().SetLabelSize(0.035)

pythia_hist.GetXaxis().SetTitleOffset(1.05)
pythia_hist.GetYaxis().SetTitleOffset(1.05)


nbins = pythia_hist.GetNbinsX()
xmiddles = [pythia_hist.GetBinCenter(b) for b in range(1, nbins+1)]
data = [pythia_hist.GetBinContent(b) for b in range(1, nbins+1)]
errors = [math.sqrt(d) for d in data]

gr = TGraph(nbins, array("d", xmiddles), array("d", data))
gr.SetMarkerStyle(8)
gr.SetMarkerSize(0.5)
gr.SetMarkerColor(1)
#gr = TGraphErrors(nbins, array("d", xmiddles), array("d", data), array("d", [0,]*nbins), array("d", errors))
#ROOT.IABstyles.h1_style(gr, ROOT.IABstyles.lWidth//2, ROOT.IABstyles.Scolor, 1, 0, 0, -1111, -1111, 508, 508, 8, ROOT.IABstyles.Scolor, 0.1, 0)
#
#gr_fit = TGraph(nbins, array("d", xmiddles), array("d", data))
#ROOT.IABstyles.h1_style(gr, ROOT.IABstyles.lWidth//2, 632, 1, 0, 0, -1111, -1111, 505, 505, 8, 632, 0.1, 0)

pythia_hist.Draw("axis")
gr.Draw("P")
#gr_fit.Draw("c")


canvas.SaveAs("pythia_background.png")
canvas.SaveAs("pythia_background.pdf")


##################################################################################################################
##################################################################################################################
##################################################################################################################


canvas2 = TCanvas("peak", "peak", 0, 0, 600, 450)
#canvas2.SetLogy(True)
canvas2.SetBottomMargin(0.11)
canvas2.SetLeftMargin(0.11)
canvas2.SetTopMargin(0.05)
canvas2.SetRightMargin(0.05)

peak_file = TFile.Open("Fourth_Year_Data/QStar/dataLikeHistograms.QStar3000.root")
nominal = peak_file.GetDirectory("Nominal")
peak_hist = nominal.Get("mjj_Scaled_QStar3000_30fb")

peak_hist.SetTitle("")

peak_hist.GetYaxis().SetTitle("q* Events")
peak_hist.GetYaxis().SetTitleSize(0.04)
peak_hist.GetYaxis().SetLabelSize(0.035)
#peak_hist .GetYaxis().SetNdivisions(508)

peak_hist.GetXaxis().SetTitleSize(0.04)
peak_hist.GetXaxis().SetLabelSize(0.035)
peak_hist.GetXaxis().SetRangeUser(0, 6000)

peak_hist.GetXaxis().SetTitleOffset(1.05)
peak_hist.GetYaxis().SetTitleOffset(1.2)

peak_hist.Draw()

canvas2.SaveAs("peak_qstar_3000.png")
canvas2.SaveAs("peak_qstar_3000.pdf")

"""canvas = TCanvas(particle, particle, 0, 0, 600, 550)
canvas.SetLogy(True)
#canvas.SetLeftMargin(0.15)
gPad.SetTicky(2)
gPad.SetTickx(1)


x = array("d", list(map(itemgetter(0), brazil_data)))
mean = array("d", list(map(itemgetter(1), brazil_data)))
xerr = array("d", [0,]*len(brazil_data))
rms = array("d", list(map(itemgetter(2), brazil_data)))
rms2 = array("d", [2*r for r in rms])
low_2sigma = array("d", list(map(itemgetter(3), brazil_data)))
low_1sigma = array("d", list(map(itemgetter(4), brazil_data)))
high_1sigma = array("d", list(map(itemgetter(5), brazil_data)))
high_2sigma = array("d", list(map(itemgetter(6), brazil_data)))

mg = TMultiGraph()
#mg.SetTitle(title)

brazil_yellow = TGraphAsymmErrors(len(brazil_data), x, mean, xerr, xerr, low_2sigma, high_2sigma)
brazil_yellow.SetFillColor(5)
brazil_yellow.SetFillStyle(1001)
brazil_yellow.SetLineColor(3)
brazil_yellow.SetLineWidth(10)
brazil_yellow.SetMarkerColor(3)


brazil_green = TGraphAsymmErrors(len(brazil_data), x, mean, xerr, xerr, low_1sigma, high_1sigma)
brazil_green.SetFillColor(3)
brazil_green.SetFillStyle(1001)
brazil_green.SetLineColor(3)
brazil_green.SetLineWidth(3)


mg.Add(brazil_yellow)
mg.Add(brazil_green)
mg.Draw("a3")

mg.GetXaxis().SetTitle("Mass [GeV]")
mg.GetYaxis().SetTitle("#sigma #times A #times BR [pb]")
mg.GetYaxis().SetRangeUser(*y_limits)
mg.GetYaxis().SetTitleOffset(1.3)
mg.GetXaxis().SetNdivisions(508)

brazil_line = TGraph(len(brazil_data), x, mean)
brazil_line.SetLineStyle(7)
brazil_line.SetLineColor(1)
brazil_line.Draw("same")

data_mass_limit_pairs = []
with open(data_cl_file, "r") as data_file:
    for line in data_file.readlines():
        data_mass_limit_pairs.append(tuple(map(float, line.split(":"))))

data_x, data_y = zip(*sorted(data_mass_limit_pairs, key=itemgetter(0)))
data_y = [dy/fb2 for dy in data_y]
data_line = TGraph(len(data_x), array("d", data_x), array("d", data_y))
data_line.SetLineStyle(1)
data_line.SetLineColor(1)
data_line.SetLineWidth(2)
data_line.SetMarkerStyle(8)
data_line.SetMarkerSize(0.75)
data_line.SetMarkerColor(1)
data_line.Draw("samePL")

print(mass_points)
theory_x = list(mass_points)
theory_y = []
for m in theory_x:
    root_file = TFile.Open(sim_file.format(m))
    nominal = root_file.GetDirectory("Nominal")
    hist = nominal.Get(sim_hist.format(m))
    theory_y.append(hist.Integral()/30/1000)
theory_line = TGraph(len(theory_x), array("d", theory_x), array("d", theory_y))
theory_line.SetLineStyle(9)
theory_line.SetLineColor(4)
theory_line.SetLineWidth(2)
theory_line.Draw("same")

x_intersect = 0
y_intersect = 0

for x1, x2, data1, theory1, data2, theory2 in zip(theory_x, theory_x[1:], data_y, theory_y, data_y[1:], theory_y[1:]):
    if data1 < theory1 and data2 > theory2:
        data1, theory1, data2, theory2 = math.log(data1), math.log(theory1), math.log(data2), math.log(theory2)
        print("Setting intersect")
        x = (theory1-data1)/((data2-data1-theory2+theory1)/(x2-x1))
        x_intersect = x1+x
        y_intersect = math.exp(theory1 + x*(theory2-theory1)/(x2-x1))

print("observed x intersect: {0}".format(x_intersect))
print("observed y intersect: {0}".format(y_intersect))

intersect_line = TGraph(1, array("d", [x_intersect,]), array("d", [y_intersect,]))
intersect_line.SetMarkerStyle(8)
intersect_line.SetMarkerSize(0.6)
intersect_line.SetMarkerColor(2)
#intersect_line.Draw("same P")

label = ROOT.TText()
label.SetNDC()
label.SetTextSize(0.04)
label.SetTextFont(42)
#label.DrawText(0.13, 0.85, "Observed data/theory intersect: {0:.0f} GeV".format(x_intersect))




exp_x_intersect = 0
exp_y_intersect = 0

for x1, x2, sim1, theory1, sim2, theory2 in zip(theory_x, theory_x[1:], mean, theory_y, mean[1:], theory_y[1:]):
    if sim1 < theory1 and sim2 > theory2:
        sim1, theory1, sim2, theory2 = math.log(sim1), math.log(theory1), math.log(sim2), math.log(theory2)
        print("Setting intersect")
        x = (theory1-sim1)/((sim2-sim1-theory2+theory1)/(x2-x1))
        exp_x_intersect = x1+x
        exp_y_intersect = math.exp(theory1 + x*(theory2-theory1)/(x2-x1))

print("expected x intersect: {0}".format(exp_x_intersect))
print("expected y intersect: {0}".format(exp_y_intersect))

intersect_line1 = TGraph(1, array("d", [exp_x_intersect,]), array("d", [exp_y_intersect,]))
intersect_line1.SetMarkerStyle(8)
intersect_line1.SetMarkerSize(0.6)
intersect_line1.SetMarkerColor(2)
#intersect_line1.Draw("same P")

label = ROOT.TText()
label.SetNDC()
label.SetTextSize(0.04)
label.SetTextFont(42)
#label.DrawText(0.13, 0.8, "Expected data/theory intersect: {0:.0f} GeV".format(exp_x_intersect))


ATLAS_label = ROOT.TText()
ATLAS_label.SetNDC()
ATLAS_label.SetTextSize(0.04)
ATLAS_label.SetTextFont(72)
#ATLAS_label.DrawText(0.575, 0.7, "ATLAS preliminary")
ATLAS_label.DrawText(0.575, 0.84, "ATLAS preliminary")


label = ROOT.TLatex()
label.SetNDC()
label.SetTextSize(0.04)
label.SetTextFont(42)
#label.DrawLatex(0.575, 0.645, "#sqrt{s} = 13 TeV, 70fb^{-1}")
label.DrawLatex(0.575, 0.785, "#sqrt{s} = 13 TeV, %sfb^{-1}" % str(fb))


legend = TLegend(0.125, 0.125, 0.6, 0.3)
legend.SetMargin(0.15)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.AddEntry(theory_line, particle_symbol, "l")
legend.AddEntry(data_line, "Observed 95% CL upper limit", "lp")
legend.AddEntry(brazil_line, "Expected 95% CL upper limit", "l")
legend.AddEntry(brazil_yellow, "Expected #pm 1#sigma and #pm 2#sigma")
legend.Draw()


if not op.exists("plt{0}".format(job_id)):
    os.mkdir("plt{0}".format(job_id))
canvas.SaveAs("plt{0}/brazil-{0}.png".format(job_id))
canvas.SaveAs("plt{0}/brazil-{0}.pdf".format(job_id))

with open("plt{0}/limits.txt".format(job_id), "w") as limit_file:
    limit_file.write("Observed mass limit: {0} GeV\n".format(x_intersect))
    limit_file.write("Observed cross section limit: {0} pb\n".format(y_intersect))
    limit_file.write("Expected mass limit: {0} GeV\n".format(exp_x_intersect))
    limit_file.write("Expected cross section limit: {0} pb\n".format(exp_y_intersect))
    """
