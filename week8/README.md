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

#### Fitting

A variable `model_scale_values` is added to the Fits class, which stores the bin contents
of the model peak. In the fitting function we then combine these values with the background
to fit to the data.

```python
model_val += self.model_scale_values[i]*par[4]
```

par[4] is the parameter used to fit the peak. It is almost always 1, as the randomly generated
peak should pretty much follow the shape of the scaled histogram used as a basis for the
random generation.

From here the process involves generating a huge number of random distributions for different
amounts of injected events and seeing how many outliers we get. This means that the whole
thing needs to be set up to be automated, because running this manually that many times
is entirely out of the question.

Rather than outputting the canvas as a png at the end of `fit_mass()`, let's have it return the
number of events that our fit suggests are in the peak. After the fitting is complete,
we can get par[4] from TMinuit and use this to scale the simulated peak by, and then
integrate that to get a number of events.

In fact, let's start in a whole new function so we can leave the plotting code as is.
We'll call it `fit_peak`, and it will do everything `fit_mass` did up to and including
initiating the fitting algorithm, but none of the plotting. Following that we only need
to add these lines

```python
par4 = ROOT.Double(0)
par4_error = ROOT.Double(0)

fits.gMinuit.GetParameter(4, par4, par4_error)

hist_model.Scale(par4)
return hist_model.Integral()
```

Then we need a function that will automate this, for now it will just print one trial run.

```python
def fit_many():
    print(fit_peak(40000))
```

```
(root-py2)[thartland@lapa week8]$ python fit_mass_qstar.py
40695.500592
```

Also let's time that.

```
(root-py2)[thartland@lapa week8]$ time python fit_mass_qstar.py
39973.6158615

real    0m8.096s
user    0m5.289s
sys 0m0.463s
```

So we're at 8 seconds per trial. If I wanted to do 1000 trials just for one input value, that
alone would take almost 2.5 hours at this rate. Maybe it's time to start setting this up
as a batch process to run in parallel. For now, I'll try 100 trials and see where that gets me.

By the way, this is what the fit looks like for 40000 events.

![image](https://github.com/H4rtland/masters/blob/master/week8/imgs/output_qstar_40000.png "")

It's a smaller bump than what we were working with earlier. Also, this line is fairly useful to
include now.

```python
self.gMinuit.SetPrintLevel(-1)
```

This suppresses the output of the fitting process. Since we're going to be running this over
and over again there's no point having any output. There is still an error output if it
can't reach the target tolerance though, which might be problematic. For 40000 that shouldn't
be an issue so for now I can just print the results to stdout and redirect that to a file.
Or, maybe I should write the file myself so that I can have debug information about how
far in we are printed out every x trials.

This is what we will test now. Results are written to a file, and the `LoadMacro` calls
have been moved into `fit_many` so they are only called once.

```python
def fit_many():
    start_time = time.time()
    gROOT.LoadMacro("FitFunction.cpp+g")
    gROOT.LoadMacro("IABStyle.cpp+g")
    with open("results.txt", "w") as out_file:
        for i in range(0, 100):
            if i%10 == 0:
                print("Starting trial {0}".format(i))
            n = fit_peak(40000)
            out_file.write("{0}\n".format(n))

    print("Took {0:.2f} seconds in total".format(time.time()-start_time))
```
