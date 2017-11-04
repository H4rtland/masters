### Week 2
###### October 30th - November 5th 2017

#### First look at rootpy
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

#### Rewriting z_read_root.cpp to rootpy

Well, I've been at it all day and I can't seem to get rootpy histograms to stop looking like they do in the plot above,
and to start looking like the output of z_read_root.cpp.

I've tried opening the z_mass.root file produced by the C++ version in rootpy so that I can take a look at the internals,
and from what I can tell, the output of the rootpy version is styled exactly the same as the C++ one.

If I draw the histogram before writing it to the .root file, it looks exactly right.
But when I load it up from the file, even if it's through rootpy rather than a TBrowser, it looks wrong.
