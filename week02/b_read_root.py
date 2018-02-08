import math

from ROOT import TH1D, TFile


root_file = TFile.Open("b_mass.root", "recreate")

b_mass_hist = TH1D("b_mass", "B mass", 50, 4.5, 6)
b_mass_more_bins = TH1D("b_mass_more_bins", "B mass", 100, 4.5, 6)

with open("fourVectorsHuge.txt", "r") as data_file:
    with open("b.out", "w") as output_file:
        for line in data_file.readlines():
            if len(line.strip()) == 0: break
            
            data = map(float, line.split())
            
            p1, e1, p2, e2, p3, e3 = data[0:3], data[3], data[4:7], data[7], data[8:11], data[11]
            
            eb = e1 + e2 + e3
            pb = [a+b+c for a,b,c in zip(p1, p2, p3)]
            
            mb = math.sqrt(reduce(lambda x, y: x-y**2, pb, eb**2))
            
            b_mass_hist.Fill(mb)
            b_mass_more_bins.Fill(mb)
            
            output_file.write("{0}\n".format(mb))

b_mass_hist.Write()
b_mass_more_bins.Write()

root_file.Close()
