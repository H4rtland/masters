## Week 12
###### February 12th-18th 2018

### Batch system

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


