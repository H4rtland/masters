# read_test.py
# Try reading out the data points from the root data file

from __future__ import print_function

from ROOT import TFile

root_file = TFile.Open("Fourth_Year_Data/mjj_data15_13TeV_00276262_physics_Main_total_final.root")

hist = root_file.Get("mjj_data15_13TeV_00276262_physics_Main_total_final")

print("Total number of bins", hist.GetNbinsX())
print()

for b in range(1, hist.GetNbinsX()+1):
    print("Value in bin {0}: {1}".format(b, hist.GetBinContent(b)))
    print("Bin {0} Left={1} Center={2} Right={3}".format(b,
                                                         hist.GetBinLowEdge(b),
                                                         hist.GetBinCenter(b),
                                                         hist.GetBinLowEdge(b+1)))
    print()
