from __future__ import print_function, division

import sys
import math
import os
import os.path as op
from array import array
from operator import itemgetter

if len(sys.argv) <= 1:
    print("Usage: python plot_limit_dist.py results/job_id")
    sys.exit()

import ROOT
from ROOT import TH1D, TCanvas, gROOT, gPad, TGraph, TGraphErrors, TGraphAsymmErrors, TMultiGraph, TFile, TRandom

gROOT.SetBatch(True)

base_path = sys.argv[1]
job_id = op.split(base_path)[1]

with open(op.join(base_path, "desc.txt"), "r") as desc_file:
    title, particle = desc_file.readline().strip().split(",")
    sim_file = desc_file.readline().strip()
    sim_hist = desc_file.readline().strip()

print("Title: {0}".format(title))
print("Particle: {0}".format(particle))
print("Sim file: {0}".format(sim_file))
print("Sim hist: {0}".format(sim_hist))

y_limits = {
    "q*": (1e-4, 4),
    "qbh": (1e-5, 1e-1),
    "wprime": (5e-5, 4),
}[particle]

data_cl_file = {
    "q*":     "results/data_cl_dist_qstar.txt",
    "qbh":    "results/data_cl_dist_qbh.txt",
    "wprime": "results/data_cl_dist_wprime.txt",
}[particle]

brazil_data = [] # (mass, mean, rms) tuples
data_mass = []
data_mean = []
data_rms = []
data_2sl = [] # 2 sigma low
data_1sl = [] # 1 sigma low
data_1sh = [] # 1 sigma high
data_2sh = [] # 2 sigma high

mass_points = []

for mass_folder in sorted(os.listdir(base_path)):
    if not mass_folder.isdigit():
        continue

    mass = int(mass_folder)

    mass_points.append(mass)

    if mass < 2000:
        continue
    binsize = 5
    bin_end = 10000
    if mass >= 4000:
        binsize = 1
        bin_end = 2000
    if mass >= 5000:
        binsize = 0.2
        bin_end = 1000
    if mass >= 6000:
        binsize = 0.1
        bin_end = 500
    if mass >= 6500:
        binsize = 0.05
        bin_end = 250
    
    bins = int(bin_end/binsize)
    hist = TH1D("dist{0}".format(mass), "dist", bins, 0, bin_end)
    r = TRandom()
    for result_file_name in os.listdir(op.join(base_path, mass_folder)):
        with open(op.join(base_path, mass_folder, result_file_name), "r") as result_file:
            for line in result_file.readlines():
                if len(line) == 0:
                    continue
                limit = float(line)
                hist.Fill(69*limit/r.Gaus(69, 0.032*69))
    
    mean = hist.GetMean()
    rms = hist.GetRMS()
    
    one_sigma = 0.3173
    two_sigma = 4.55e-2
    
    low_2sigma = None
    low_1sigma = None
    high_1sigma = None
    high_2sigma = None

    bin_content = [hist.GetBinContent(b) for b in range(1, hist.GetNbinsX()+1)]
    bin_locations = [hist.GetBinCenter(b) for b in range(1, hist.GetNbinsX()+1)]
    # cumulative = [sum(bin_content[0:b]) for b in range(0, len(bin_content))]
    cumulative = []
    current_sum = 0
    for content in bin_content:
        cumulative.append(current_sum)
        current_sum += content
    cumulative.append(current_sum)
    binsize = 1
    cumulative = [c/max(cumulative) for c in cumulative]
    m = None
    for x, y in zip(bin_locations, cumulative):
        if y >= two_sigma/2 and low_2sigma is None:
            low_2sigma = abs(x-mean)
            if mass == m:
                print(x, y, two_sigma/2)
        if y >= one_sigma/2 and low_1sigma is None:
            low_1sigma = abs(x-mean)
            if mass == m:
                print(x, y, one_sigma/2)
        if y >= 1-(one_sigma/2) and high_1sigma is None:
            high_1sigma = abs(x-mean)
            if mass == m:
                print(x, y, 1-one_sigma/2)
        if y >= 1-(two_sigma/2) and high_2sigma is None:
            high_2sigma = abs(x-mean)
            if mass == m:
                print(x, y, 1-two_sigma/2)


    brazil_data.append((mass, mean, rms, low_2sigma, low_1sigma, high_1sigma, high_2sigma))

mass_points = sorted(mass_points)

brazil_data = sorted(brazil_data, key=itemgetter(0))
brazil_data = [(x, m/69000, r/69000, a/69000, b/69000, c/69000, d/69000) for x, m, r, a, b, c, d in brazil_data]

canvas = TCanvas(particle, particle, 0, 0, 500, 450)
canvas.SetLogy(True)
gPad.SetTicky(2)

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
mg.SetTitle(title)

brazil_yellow = TGraphAsymmErrors(len(brazil_data), x, mean, xerr, xerr, low_2sigma, high_2sigma)
brazil_yellow.SetFillColor(5)
brazil_yellow.SetFillStyle(1001)
brazil_yellow.SetLineColor(3)
brazil_yellow.SetLineWidth(3)


brazil_green = TGraphAsymmErrors(len(brazil_data), x, mean, xerr, xerr, low_1sigma, high_1sigma)
brazil_green.SetFillColor(3)
brazil_green.SetFillStyle(1001)
brazil_green.SetLineColor(3)
brazil_green.SetLineWidth(3)


mg.Add(brazil_yellow)
mg.Add(brazil_green)
mg.Draw("a3")

mg.GetXaxis().SetTitle("Mass (GeV)")
mg.GetYaxis().SetTitle("#sigma #times A #times BR [pb]")
mg.GetYaxis().SetRangeUser(*y_limits)

brazil_line = TGraph(len(brazil_data), x, mean)
brazil_line.SetLineStyle(7)
brazil_line.SetLineColor(1)
brazil_line.Draw("same")

data_mass_limit_pairs = []
with open(data_cl_file, "r") as data_file:
    for line in data_file.readlines():
        data_mass_limit_pairs.append(tuple(map(float, line.split(":"))))

data_x, data_y = zip(*sorted(data_mass_limit_pairs, key=itemgetter(0)))
data_y = [dy/69000 for dy in data_y]
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

print("x intersect: {0}".format(x_intersect))
print("y intersect: {0}".format(y_intersect))

intersect_line = TGraph(1, array("d", [x_intersect,]), array("d", [y_intersect,]))
intersect_line.SetMarkerStyle(8)
intersect_line.SetMarkerSize(0.5)
intersect_line.SetMarkerColor(2)
intersect_line.Draw("P")

label = ROOT.TText()
label.SetNDC()
label.SetTextSize(0.04)
label.SetTextFont(42)
label.DrawText(0.13, 0.85, "Data/theory intersect: {0:.0f} GeV".format(x_intersect))

if not op.exists("plt{0}".format(job_id)):
    os.mkdir("plt{0}".format(job_id))
canvas.SaveAs("plt{0}/brazil-{0}.png".format(job_id))
canvas.SaveAs("plt{0}/brazil-{0}.pdf".format(job_id))
