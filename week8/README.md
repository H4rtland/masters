## Week 8
###### January 15th-21st 2018

### Signal injection test

In which a randomly generated signal is added to a randomly generated background distribution.
The regular analysis is then run to try to recover the input signal
for signals of varying sizes. Each signal size is tested many times.
From this information we can see how many times you would expect to find
a signal when the input size was zero, for example.

Well, I've just spent about 3 hours implementing this, of which at least 2 hours and 30 minutes
can be attributed to pure stupidity on my part. The data/model histograms are on an x-axis of
GeV, when viewed in ROOT. As part of the loading process in my code, these values are scaled
to TeV. Which means that when suggesting an initial value to the fitting code, you would want
to use **3** rather than **3000** as the mean for a gaussian peak on top of the background. 

In the process of getting this right, I produced about a million of these graphs

![image](https://github.com/H4rtland/masters/blob/master/week8/imgs/output_qstar_bad.png "")

And after realising my mistake eventually ended up with one of these.

![image](https://github.com/H4rtland/masters/blob/master/week8/imgs/output_qstar_good.png "")

The gaussian peak is slightly mismatched on the higher energy tail, as the q\* distribution
has more of a sharp falloff on this edge, rather than gauss-like.

The overall method for this first iteration of the background+peak fitting is:

1. Add three new parameters to the fitting function which are the scale, mean and standard
deviation of a gaussian function. The gaussian is added to FitFunction.cpp

```cpp
// pars[4] scale factor
// pars[5] mean
// pars[6] standard deviation
Double_t arg4 = 0;
if (pars[6] != 0) {
    arg4 = (x - pars[5]) / pars[6];
}
Double_t arg5 = pars[4] * TMath::Exp(-0.5*arg4*arg4);

return (arg1 * arg3) + arg5;
```

Where (arg1 * arg3) is the background as previously, and arg5 is the gaussian added to it.

2. The Fit class in the python code has a variable `exclude_regions` added to it.
This is a list of (lower_bound, higher_bound) pairs, and when fitting, any x value
in between any of the pairs will be excluded. Having this as a variable means we can
change it in the fitting process, so that we can exclude the peak to fit the background,
and then exclude the background to fit the peak.

3. The fitting is performed first by fixing all parameters and unlocking the background
parameters one by one, and then by relocking all the background parameters and unlocking
the gaussian parameters one by one. The excluded regions are changed according to which
section is being fitted.

A better approach, which fixes our issue of the q\* being non-gaussian, is to simply fit
the peak to a scaled version of the peak model's histogram. This feels a lot like cheating,
but it's a valid tactic even when fitting actual data, as the shape of an actual q\* peak
should match the shape of a simulated q\* peak. This also reduces the number of extra fitting
parameters to one, as we only need to fit the height of the distribution, rather than
the scale, mean, sigma values which were necessary for fitting a gaussian.

Also, I had confused myself by adding the gaussian code to the C++ fitting code, as the
GaussIntegrator is only necessary to get an accurate value of the background taking into
account the entire width of the bin, and the gaussian could have been implemented in pure
python. 

In the next version of the code, the peak histogram bin values will be given to
the fitting class, and will be combined with a single parameter par[4] which will be
optimised to fit the model peak to the "data" peak on top of the background.
At this point, the optimisation shouldn't have to do anything at all because the "data"
peak is just the model we injected, but first we will change the code to generate a
random background and random peak each time.

#### Random distribution generation

Starting with our two distributions, the background `hist` and the simulated q\*
distribution `hist_model`. First the model is smoothed, normalised, and scaled
to a given number of events.

```python
hist_model.Smooth(1)
hist_model.Scale(1/hist_model.Integral())
hist_model.Scale(40000)
```

We then overwrite the bin contents in `hist` with a random background + random peak.
The background is modelled using previously fitted parameters for just the background.

```python
class BackgroundModel:
    def __init__(self, p1, p2, p3, p4):
        self.p1, self.p2, self.p3, self.p4 = p1, p2, p3, p4

    def model_at(x):
        scale = x/14
        a1 = self.p1 * math.pow(1-scale, self.p2)
        a2 = self.p3 * (self.p4 * math.log(scale))
        a3 = math.pow(scale, a2)
        return a1*a3

    def random_at(self, x):
        return poisson.ppf(random.random(), self.model_at(x))
```

After initialising a background model

```python
background = BackgroundModel(1.70475e1, 8.43990, -4.63149, -2.43023e-3)
```

we can generate random background values for a given Mjj. Random peak values are generated
in the same way, only using the `hist_model` for the mean value of the poisson distribution.
Then, we can start overwriting the bins in `hist`.

```python
for b in range(1, hist.GetNBinsX()+1):
    if hist.GetBinContent(b) > 0 or hist.GetBinLowEdge(b)/1000 > 2:
        x = hist.GetBinCenter(b)/1000
        bg = background.random_at(x)
        peak = 0
        if hist_model.GetBinContent(b) > 0:
            peak = poisson.ppf(random.random(), hist_model.GetBinContent(b))
        hist.SetBinContent(b, bg+peak)
```

The first `if` makes sure that we aren't generating values where there is no background
data on the very left of the distribution, and the second `if` is there because supplying
a mean of 0 to poisson.ppf makes it return NaN, which we would have to ignore anyway,
so we leave the value at 0.

If all of the `peak` values are added up, it can be confirmed that the number of injected
events matches the number used to scale the simulated distribution after it has been normalised.

From here, `hist` can be used for fitting as usual. Now we don't need to add the two histograms
together as we were doing before (`hist.Add(hist_model)`) because we're doing it on a bin
by bin basis.
