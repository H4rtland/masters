## Week 5
###### November 20th-26th 2017

### Modifying fit to use error of model

This is just a small change, only this

```python
chiValue = (self.data[i]-val)/self.errors[i]
```

to this

```python
chiValue = (self.data[i]-val)/math.sqrt(val)
```

The reasoning behind this is that for histogram bins with error sqrt(N),
a bin with a number of events slightly higher than the model will contribute
less to the total chi^2 value than a bin which is lower by exactly the same amount,
because the errors are different. This leads to the fit being dragged down slightly.
Using the square root of the number of events predicted by the model negates this effect.

### Excluding a range of data from the fit

This can be done by making the chi^2 calculating loop continue to the next iteration
whenever we find that the x-axis value of the bin falls within the range
we want to exclude. I chose to only compare the left edge of the bin for simplicity,
and this is probably fine. We might get a little bit of overlap into the exluded region
on the left edge, and exclude a bit of the non-excluded data on the right edge of
the exclusion zone, but the resolution of the bins compared to the width of the
excluded zone is small enough that the difference is negligible. I'm just choosing my
excluded regions by eye anyway so it's not an exact science yet.

```python
val = ig.Integral(self.xmins[i], self.xmaxes[i])/(self.xmaxes[i]-self.xmins[i])
self.data_fits[i] = val

if self.xmins[i] > 5:
    continue
```

excludes the invariant mass region M_jj > 5 TeV. The line `self.data_fits[i] = val`
had to be moved up from the bottom of the loop block to just below the calculation
of `val`, because this value needs to be set even when we are ignoring the chi^2.
This is because `data_fits` is what is plotted in the end as the red fit line.

Excluding M_jj > 5 TeV had a small effect on the parameters of the fit.

```
  INCLUDING ALL DATA

  EXT PARAMETER                APPROXIMATE        STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  p1           1.95786e+01   8.27784e-01   2.35249e-01  -6.24676e+01
   2  p2           8.65694e+00   7.02276e-02   2.16192e-02   1.18246e+02
   3  p3          -4.55654e+00   2.68376e-02   5.67888e-03   2.87279e+03
   4  p4           8.32166e-03   5.22098e-03   6.06558e-04  -6.88779e+03
```

```
  EXCLUDING M_jj > 5 TeV

  EXT PARAMETER                APPROXIMATE        STEP         FIRST
  NO.   NAME      VALUE            ERROR          SIZE      DERIVATIVE
   1  p1           1.70475e+01   5.54536e-01   2.62347e-02   3.42451e+00
   2  p2           8.43990e+00   5.31178e-02   1.80851e-03   1.22584e+00
   3  p3          -4.63149e+00   2.45655e-02   9.45773e-04  -2.17073e+02
   4  p4          -2.43023e-03   5.47424e-03   1.68411e-04   6.54767e+02
```

This wasn't enough to notice by eye unless switching back and forth between the two plots
in the same place on the screen. To check that it was actually working as intended, I
added in some code to add a random gaussian distribution on top of the background,
and then exluded this region.

```python
# Original data setup
fits = Fits()
fits.xmins = [hist.GetBinLowEdge(b)/1000 for b in range(1, nbins+1)]
fits.xmaxes = [hist.GetBinLowEdge(b+1)/1000 for b in range(1, nbins+1)]
fits.data = [hist.GetBinContent(b) for b in range(1, nbins+1)]

# New code to add gaussian on top
import random
for i in range(0, nbins-1):
    if 1.5 < fits.xmins[i] < 3.5:
        for k in range(0, 30000):
            if fits.xmins[i] < random.gauss(2.5, 0.1) < fits.xmaxes[i]:
                fits.data[i] += 1
```

![image](https://github.com/H4rtland/masters/blob/master/week5/imgs/output_gauss.png "")

I set the fitting function to exclude between 2 and 3 TeV, and clearly it is working
as intended. It would be great if excited quarks / quantum black holes / etc. made
a signal that was that easy to spot. 

### Generating a sample distribution

I spent a while trying to figure out how to invert the poisson function, but it turns out that
there's a scipy function for exactly that. Glad I'm not stuck with C++.

For generating a sample number of events for each bin, we can choose a random number between 0 and 1,
and select a number of events in a bin such that the integral of the poisson distribution up to
that number of events gives an area equal to the random number.

![image](https://github.com/H4rtland/masters/blob/master/week5/imgs/eqn1.png "")

To find k in this equation, we use the 


### Resources

Generate equations to embed in markdown  
https://www.codecogs.com/latex/eqneditor.php
