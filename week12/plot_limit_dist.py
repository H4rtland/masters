import sys
import os
import os.path as op

if len(sys.argv) <= 1:
    print("Usage: python plot_limit_dist.py results/job_id/mass/*")
    sys.exit()

import ROOT
from ROOT import TH1D, TCanvas, gROOT

gROOT.SetBatch(True)

job_id = op.splitext(op.basename(sys.argv[1]))[0]
job_id = job_id.split("job-")[1]
mass = int(job_id.split("-")[1])
job_id = job_id.split(".")[0]

limits = []

for result_file_name in sys.argv[1:]:
    with open(result_file_name, "r") as result_file:
        for line in result_file.readlines():
            if len(line) == 0:
                continue
            if "None" in line:
                continue
            limit = float(line)
            limits.append(limit)


binsize = 20
if mass >= 4000:
    binsize = 10
if mass >= 5000:
    binsize = 5
if mass >= 6000:
    binsize = 1
bins = int(10000/binsize)

canvas = TCanvas("dist", "dist", 0, 0, 650, 450)
hist = TH1D("dist", "95% C.L dist", bins, 0, 10000)

for l in limits:
    hist.Fill(l)

hist.GetXaxis().SetRangeUser(max(0, min(limits)-100), max(limits)+100)
hist.Draw()

if not op.exists("plt{0}".format(job_id)):
    os.mkdir("plt{0}".format(job_id))
canvas.SaveAs("plt{0}/95pcCL_dist_{0}-{1}.png".format(job_id, mass))
