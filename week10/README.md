## Week 10
###### January 29th - February 4th 2018

### Statistics of signal injection test continued

This week starts out with a major success: the GausIntegrator warnings have been defeated!
And not just by setting some warning level, the problem has been fixed altogether.
The root of the issue was that at low values on the x-axis, the function that the
GausIntegrator was working with didn't behave nicely. The low values exist because there
are bins in the data that go that low, even though the bins are empty there.
By counting up the 0 event bins until we reach the first data, and then by removing that number
of bins from the start of each data, errors, widths, etc. list, the problem x-axis values
are ignored.

So, where we were at last week was we had this distribution

![image](https://github.com/H4rtland/masters/blob/master/week9/imgs/L_ratio_dist.png "")

Clearly this is not the gaussian distribution we were expecting. The distribution can be
transformed into the shape we need by taking the exponential of the negative likelihood
exp(-likelihood). This converts the likelihood to a probability.

First let's take care of some other things. The fit function can be rewritten slightly.

```python
for i in range(0, self.num_bins):
    for lower, higher in self.exclude_regions:
        if lower < self.xmins[i] < higher:
            continue

    model_val = ig.Integral(self.xmins[i], self.xmaxes[i]) / (self.xmaxes[i]-self.xmins[i])
    self.background_fit_only[i] = model_val
    model_val += self.model_scale_values*par[4]
    self.data_fits[i] = model_val
    
    likelihood += model_val - self.data[i]
    if self.data[i] > 0:
        likelihood += self.data[i]*(math.log(self.data[i])-math.log(model_val))

fcnVal[0] = likelihood
```

This uses an improved likelihood for binned, poisson distributed data, and no longer includes
checks to skip over 0 event bins at low x-axis values (because we have removed them).
We also keep track of the background fit, before adding the peak. This is so that we can
iterate over different size peaks later, adding them to the background which we save here,
and comparing the result to the data. 

That function will be called `calc_likelihood`, and will take an argument `peak_scale`.
It computes the likelihood of a given size peak based on the operations I just described above.

```python
def calc_likelihood(self, peak_scale):
    like = 0

    for i in range(0, self.num_bins):
        if self.data_fits[i] <= 0:
            continue

        p = peak_scale*self.model_scale_values[i]
        tmp = ROOT.TMath.PoissonI(self.data[i], self.background_fit_only[i]+p)
        if tmp == 0:
            logtmp = math.log(sys.float_info.min)
        else:
            logtmp = math.log(tmp)
        like += logtmp

    return -like
```

The function TMath.PoissonI, which has a capital i, not a lowercase L (yes, the ROOT
documentation uses a font which makes it impossible to tell the difference), takes two parameters,
the second of which is a mean for the poisson distribution, and the first of which is the x-value
to evaluate the probability at. This is what we will be using to calculate the probability
of a given theortical peak being able to generate the data we see. As the fitting has now
been removed from this step in favour of just iterating through different peak sizes
and just calculating the likeihood only, there should also be a significant performance gain here.

The loop that now goes over the different N values is now implemented like this:

```python
fitted_N = ROOT.Double(0)
self.gMinuit.GetParameter(4, fitted_N, ROOT.Double(0))
best_fit_likelihood = self.calc_likelihood(fitted_N)

for N in range(37000, 43001, 25):
    fit_likelihood = self.calc_likelihood(N)
    x_values.append(N)
    y_values.append(fit_likelihood-best_fit_likelihood)
```

And, plotting x_values and exp(-y_values) gives us our gaussian probability distribution.

![image](https://github.com/H4rtland/masters/blob/master/week10/imgs/prob_dist_40k_1.png "")

And the cherry on top is, last week it was taking around 60 seconds to produce once of these
plots with only 20 points, now it only takes 10 seconds to produce one with ~250 points.
Not running the fitting code makes that much of a difference.

It is on this distribution that we mark our 95% confidence level limits, based on the area
under the curve. Rather than do that for this plot, let's now move on to the 0 events
injection test.

![image](https://github.com/H4rtland/masters/blob/master/week10/imgs/prob_dist_0_1.png "")

For that, we get something like this. The whole distribution does shift to the left and right
depending on the exact randomly generated input, but this one is roughly central.

The next step is to produce a cumulative distribution from this. For that I'll just be
manually doing the maths in python for now.

```python
ycumulative = [sum(y[0:i]) for i in range(0, len(y))]
ycumulative = [yval/max(ycumulative) for yval in ycumulative]
```

Then I'll find the point where the cumulative y values surpass 0.95.

```python
limit_x = 0
limit_y = 0
for xv, yv in zip(x, ycumulative):
    if yv >= 0.95:
        limit_x = xv
        limit_y = yv
        break
```

And plot a cumulative distribution graph with a line to show the limit.

```python
graph = TGraph(len(x), array("d", x), array("d", ycumulative))
ROOT.IABstyles.h1_style(graph, ROOT.IABstyles.lWidth/2, ROOT.IABstyles.Scolor,
                        1, 0, 0, -1111.0, -1111.0, 508, 508, 8,
                        ROOT.IABstyles.Scolor, 0.1, 0)
graph.SetMarkerColor(4)
graph.SetMarkerStyle(3)
graph.SetMarkerSize(1.25)
graph.Draw("ap")
line = ROOT.TLine(limit_x, 0, limit_x, limit_y)
line.SetLineColor(2)
line.Draw("same")
label = ROOT.TText()
label.SetNDC()
label.SetTextSize(0.03)
label.DrawText(0.5, 0.7, "{0:.02f} confidence limit = {1:.02f} events".format(limit_y, limit_x))
canvas2.SaveAs("sig_cumsum.png")
```

Here's one I made earlier:

![image](https://github.com/H4rtland/masters/blob/master/week10/imgs/prob_dist_0_3.png "")

![image](https://github.com/H4rtland/masters/blob/master/week10/imgs/cumulative_dist_0_3.png "")

This distribution is more skewed to the positive, meaning that the random generation
must have made a small bump in the data that could be seen as a peak. Also, the peak goes much
higher than one, which probably isn't a problem because I think it should be normalised anyway.
This means that some of the N event trials were actually a better fit than the "best fit" fit
was. Interestingly, the distribution does start at *exactly* 1. Does that mean that the
"best fit" picked out a peak of 0, even when it clearly shouldn't have?
