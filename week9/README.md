## Week 8
###### January 22nd-28th 2018

### Statistics of signal injection test

Firstly I'm experimenting with enabling/disabling the final fitting stage which
unlocks all parameters. Disabling it cuts the time taken per trial by about half
but I'm not sure how to judge how much it affects the accuracy of the fit.

Looking at the output results, disabling the last stage reduces the spread of results,
and brings the average closer to the input value. I'll leave it disabled for now and once
I have a histogram of the results distribution I'll enable it again and hopefully it will
be easier to see what's going on.

```python
distribution = TH1D("dist", "dist", 60, 3700, 4300)
with open("results.txt", "w") as out_file:
    ....

canvas = TCanvas("Canvas", "Distribution Canvas", 0, 0, 650, 450)
distribution.Draw()
canvas.SaveAs("dist.png")
```

This is the first look at the distribution for 200 trials with the final fitting stage disabled:

![image](https://github.com/H4rtland/masters/blob/master/week9/imgs/dist1.png "")

And with the final fitting stage enabled:

![image](https://github.com/H4rtland/masters/blob/master/week9/imgs/dist2.png "")

The RMS is reduced by a factor half with the last stage disabled. The second distribution
seems to be more gaussian so I'll keep the code in this state for now.

The analysis process for this week is as follows:
* Set up a random background + peak
* Fit the background
* Rather than fitting the peak, set Nx to a range of set values and calculate the likeliness
of that fit accurately describing the particular distribution.
* This will be used to calculate 95% confidence level limits on the cross section, by setting
the injected number of events to 0 and iterating until we find the point where the
number of events in the fit is so high that it couldn't possibly describe the background data.

This will involve making the last fitting stage into a loop. After first fitting as normal to find
an actual best fit, we can iterate over a range of possible injected events. Again using a mean
of 40000 injected events:

```python
for N in range(35000, 45001, 500):
    self.gMinuit.DefineParameter(4, "p5", N, 0, 0, 1e12)
    self.gMinuit.FixParameter(4)
    self.gMinuit.mnexcm("simplex", arglist, 2, ierflg)
    self.gMinuit.mnexcm("MIGRAD", arglist, 2, ierflg)
    best_fit_value = ROOT.Double(0)
    self.gMinuit.mnstat(best_fit_value, ROOT.Double(0), ROOT.Double(0),
                        ROOT.Long(0), ROOT.Long(0) ROOT.Long(0))
```

We redefine the parameter because there is no way to set it to a specific value otherwise.
We then run the fit, and use mnstat to extract the best value of the fit so far, which is
stored in `best_fit_value`. The other arguments to that function just absorb some other
values that don't need to be saved.

For now the values of `N` and `best_fit_value` are then stored into lists and returned
from the function.

I now have another new main function, `fit_significance(num_injected_events)`, which runs
the fitting and those takes those lists and plots them.

```python
x, y = fits.run_mass_fit(num_injected_events)

canvas = TCanvas("dist", "dist", 0, 0, 650, 450)
graph = TGraph(len(x), array("d", x), array("d", y))
ROOT.IABstyles.h1_style(graph, ROOT.IABstyles.lWidth/2, ROOT.IABstyles.Scolor,
                        1, 0, 0, -1111.0, -1111.0, 508, 508, 8,
                        ROOT.IABstyles.Scolor, 0.1, 0)
graph.SetMarkerColor(2)
graph.SetMarkerStyle(3)
graph.SetMarkerSize(1.5)
graph.Draw("ap")
canvas.SaveAs("sig_dist.png")
```

The result of which looks like this

![image](https://github.com/H4rtland/masters/blob/master/week9/imgs/best_fit_value_dist.png "")

From here we calculate the generic test statistic

![image](https://github.com/H4rtland/masters/blob/master/week9/imgs/eqn_chi2.png "")

In this equation, mu is the variable for the number of events N which we are iterating over.
At each step of the iteration we will evaluate this chi function. The L functions are the
likelihood at the current N (mu), and at the value of N found by fitting with free
parameters, the best fit (mu hat). As we are using log likelihoods, to take the ratio
we only need to subtract the values. The theta hat in the above equation encompasses
the other parameters of our fit.

We will then calculate the significance of the fluctuation from 0, which is given by

![image](https://github.com/H4rtland/masters/blob/master/week9/imgs/eqn_q0.png "")
