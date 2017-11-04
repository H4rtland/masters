import math

import rootpy
import rootpy.io
import rootpy.plotting
from rootpy.plotting.style import get_style
from rootpy.interactive import wait


with rootpy.io.root_open("z_mass.root", "recreate") as root_file:
    z_mass_hist = rootpy.plotting.Hist(50, 50, 150,
                            name="z_mass", title="Z Mass", type="D", drawstyle="hist")
    z_mass_more_bins = rootpy.plotting.Hist(100, 50, 150,
                            name="z_mass_bins", title="Z mass", type="D", drawstyle="hist")

    z_mass_hist.linecolor = 602 # "blue"
    z_mass_hist.drawstyle = "hist"
    # z_mass_hist.fillstyle = "solid"
    # z_mass_hist.linestyle = 1
    # z_mass_hist.markerstyle = 1
    
    with open("z.dat", "r") as data_file:
        with open("z.out", "w") as output_file:
            for line in data_file.readlines():
                if len(line.strip()) == 0: break
                
                data = map(float, line.split("\t"))
                
                p1, e1, p2, e2 = data[0:3], data[3], data[4:7], data[7]
                
                ez = e1 + e2
                pz = [a+b for a, b in zip(p1, p2)]
                
                mz = math.sqrt(reduce(lambda x, y: x-y**2, pz, ez**2))
                
                z_mass_hist.fill(mz)
                z_mass_more_bins.fill(mz)
                
                output_file.write("{0}\n".format(mz))

    z_mass_hist.draw()
    wait()
    z_mass_hist.write()
