## Week 12
###### February 12th-18th 2018

### Bug hunting

The two problems I identified at the end of last week were:

* Maximum value of cumulative sum is 0
* Odd outliers at 2380 GeV

It turns out that both these problems are because the fit does not converge.
In the case of the 2380 value, this is simply 0.95\*2500. 2500 is the maximum value that
I iterated up to when testing likelihoods.

These are the plots for a distribution that returns the 2380 value.

![image](https://github.com/H4rtland/masters/blob/master/week12/imgs/plot-51309.0.i56-hist.png "")

![image](https://github.com/H4rtland/masters/blob/master/week12/imgs/plot-51309.0.i56-sig_dist.png "")

![image](https://github.com/H4rtland/masters/blob/master/week12/imgs/plot-51309.0.i56-sig_cumsum.png "")

The likelihood is a minimum everywhere which leads to the probability being 1 everywhere.
This forms a linear distribution in the cumulative sum, which is how we get 0.95\*2500 as the
resulting 95\% limit.

There's nothing I can really do about the fit not converging, so the best thing to do now
is to figure out the easiest way to just ignore the results when the fitting doesn't work.

Checking for the maximum value in the cumulative sum being 0 is easy, but for the 2380 limit
we'll need to figure out whether or not the fit converged or not. And for this we can use for
the first time the error flag that gets passed in the fitting calls. By adding a line
to print the limit and error flag after each iteration, I see that when when the limit is 2380
the error flag is 0, and when the limit is a normal value the error flag is 4. This is the exact
OPPOSITE of what the ROOT documentation suggests, which is that 0 means "command executed
normally", and 4 means "abnormal termination (e.g MIGRAD not converged)".

Unless the error flag has a value of 4, I will reject the result from now on. I have also changed
the for loop into a while loop that keeps going until it gets the desired number of successful
results. It will also stop if the total number of loops is twice the disired number of results,
so that in case something goes seriously wrong it will not just keep going forever.

### Background data

I have also changed the code so that rather than generate a random background from a distribution
function using previously fitted parameters, I am now using the smooth Pythia background from
one of the earlier weeks. However once I made this change the 95% limit shifted to the right
by quite a way. The distribution now looks like this:

![image](https://github.com/H4rtland/masters/blob/master/week12/imgs/95pcCl_dist_51309.png "")

This distribution was produced before making the changes in the above section, which is why
there is still a massive spike at 2380.
