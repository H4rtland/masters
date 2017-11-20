## Week 2
###### October 30th - November 5th 2017

### First look at rootpy
On remote machine, in ~/venvs

    $ virtualenv --system-site-packages rootpy
    $ source rootpy/bin/activate
    $ pip install --upgrade pip
    $ pip install rootpy
    $
    $ python
    >>> from rootpy.plotting import Hist
    >>> hist = Hist(10, 0, 1)
    >>> hist.FillRandom("gaus", 100000)
    >>> hist.Draw()

Draws a minimal canvas with a basic histogram on it.
It looks more like a scatter plot with large horizontal error bars.

![image](https://github.com/H4rtland/masters/blob/master/week2/imgs/first_rootpy_hist.png "Basic histogram")

### Rewriting z_read_root.cpp to rootpy

Well, I've been at it all day and I can't seem to get rootpy histograms to stop looking like they do in the plot above,
and to start looking like the output of z_read_root.cpp.

I've tried opening the z_mass.root file produced by the C++ version in rootpy so that I can take a look at the internals,
and from what I can tell, the output of the rootpy version is styled exactly the same as the C++ one.

If I draw the histogram before writing it to the .root file, it looks exactly right.
But when I load it up from the file, even if it's through rootpy rather than a TBrowser, it looks wrong.

---

Histogram looks right when drawn before saving, as `drawstyle = "hist"` isn't saved to the .root file (it's a rootpy specific attribute).
Opening the file with rootpy in python REPL and setting drawstyle again sets it back to looking right.

I'll switch back to PyROOT since this doesn't seem to have a convenient fix.
The rootpy version is now rootpy_z_read_root.py, and z_read_root.py is now PyROOT.

```python
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
```


Either PyROOT or rootpy are certainly preferable to using c++ for this type of task (for me at least). 
The performance hit isn't so bad either. On the B events data set:

```
(rootpy)[thartland@lapa week1]$ time ./b_read_root

real	0m6.955s
user	0m5.613s
sys	0m1.112s
(rootpy)[thartland@lapa week1]$ cd ../week2
(rootpy)[thartland@lapa week2]$ time python b_read_root.py 

real	0m17.898s
user	0m17.120s
sys	0m0.919s
```

On fourVectorsHuge.txt (about 700k events), that was only a ~2.5x slowdown.
That's fine for now, maybe later it will be significant.


### Resources

http://hep.lancs.ac.uk/bertram/2016-17/fourVectorsHuge.txt  
fourVectorsHuge.txt (too large to add to repository)

https://indico.cern.ch/event/567552/contributions/2301470/attachments/1339387/2016163/rootpy-talk.pdf  
Useful examples for rootpy (and PyROOT!)


