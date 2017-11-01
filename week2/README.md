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

![image](https://github.com/H4rtland/masters/blob/master/week2/imgs/first_rootpy_hist?raw=true "Basic histogram")
