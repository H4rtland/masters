import math

from ROOT import TH1D, TFile


root_file = TFile.Open("z_mass.root", "recreate")

z_mass_hist = TH1D("z_mass", "Z mass", 50, 50, 150)
z_mass_more_bins = TH1D("z_mass_bins", "Z mass", 100, 50, 150)

with open("z.dat", "r") as data_file:
    with open("z.out", "w") as output_file:
        for line in data_file.readlines():
            if len(line.strip()) == 0: break
            
            data = map(float, line.split("\t"))
            
            p1, e1, p2, e2 = data[0:3], data[3], data[4:7], data[7]
            
            ez = e1 + e2
            pz = [a+b for a,b in zip(p1, p2)]
            
            mz = math.sqrt(reduce(lambda x, y: x-y**2, pz, ez**2))
            
            z_mass_hist.Fill(mz)
            z_mass_more_bins.Fill(mz)
            
            output_file.write("{0}\n".format(mz))

z_mass_hist.Write()
z_mass_more_bins.Write()

root_file.Close()
