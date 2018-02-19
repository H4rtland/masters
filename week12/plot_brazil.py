import sys
import os
import os.path as op
from array import array
from operator import itemgetter

if len(sys.argv) <= 1:
    print("Usage: python plot_limit_dist.py results/job_id")
    sys.exit()

import ROOT
from ROOT import TH1D, TCanvas, gROOT, gPad, TGraph, TGraphErrors, TMultiGraph

gROOT.SetBatch(True)

base_path = sys.argv[1]
job_id = op.split(base_path)[1]

brazil_data = [] # (mass, mean, rms) tuples

for mass_folder in os.listdir(base_path):
    mass = int(mass_folder)
    if mass < 2000:
        continue
    binsize = 20
    if mass >= 4000:
        binsize = 10
    if mass >= 5000:
        binsize = 5
    if mass >= 6000:
        binsize = 1
    
    bins = int(10000/binsize)
    hist = TH1D("dist{0}".format(mass), "dist", bins, 0, 10000)
    
    for result_file_name in os.listdir(op.join(base_path, mass_folder)):
        with open(op.join(base_path, mass_folder, result_file_name), "r") as result_file:
            for line in result_file.readlines():
                if len(line) == 0:
                    continue
                limit = float(line)
                hist.Fill(limit)
    
    mean = hist.GetMean()
    rms = hist.GetRMS()
    brazil_data.append((mass, mean, rms))

brazil_data = sorted(brazil_data, key=itemgetter(0))
brazil_data = [(x, m/37000, r/37000) for x, m, r in brazil_data]

canvas = TCanvas("dist", "dist", 0, 0, 650, 450)
canvas.SetLogy(True)
gPad.SetTicky(2)

x = array("d", list(map(itemgetter(0), brazil_data)))
mean = array("d", list(map(itemgetter(1), brazil_data)))
xerr = array("d", [0,]*len(brazil_data))
rms = array("d", list(map(itemgetter(2), brazil_data)))
rms2 = array("d", [2*r for r in rms])

mg = TMultiGraph()
mg.SetTitle("q* 95% CL limit brazil plot")

brazil_yellow = TGraphErrors(len(brazil_data), x, mean, xerr, rms2)
brazil_yellow.SetFillColor(5)
brazil_yellow.SetFillStyle(1001)
brazil_yellow.SetLineColor(3)
brazil_yellow.SetLineWidth(3)


brazil_green = TGraphErrors(len(brazil_data), x, mean, xerr, rms)
brazil_green.SetFillColor(3)
brazil_green.SetFillStyle(1001)
brazil_green.SetLineColor(3)
brazil_green.SetLineWidth(3)


mg.Add(brazil_yellow)
mg.Add(brazil_green)
mg.Draw("a3")

mg.GetXaxis().SetTitle("Mass (GeV)")
mg.GetYaxis().SetTitle("#sigma #times A #times BR [pb]")
mg.GetYaxis().SetRangeUser(1e-4, 4)


brazil_line = TGraph(len(brazil_data), x, mean)
brazil_line.SetLineStyle(7)
brazil_line.SetLineColor(1)
brazil_line.Draw("same")

if not op.exists("plt{0}".format(job_id)):
    os.mkdir("plt{0}".format(job_id))
canvas.SaveAs("plt{0}/brazil-{0}.png".format(job_id))
