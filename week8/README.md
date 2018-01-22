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

The gaussian peak is slightly mismatched on the higher energy tail, as the qstar distribution
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

2. The Fit class in the python code has a variable `exclude_regions` added to it.
This is a list of (lower_bound, higher_bound) pairs, and when fitting any x value
in between any of the pairs will be excluded. Having this as a variable means we can
change it in the fitting process, that that we can exclude the peak to fit the background,
and then exclude the background to fit the peak.

3. The fitting is performed first by fixing all parameters and unlocking the background
parameters one by one, and then by relocking all the background parameters and unlocking
the gaussian parameters one by one. The excluded regions are changed according to which
section is being fitted.
