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
MeV, when viewed in ROOT. As part of the loading process in my code, these values are scaled
to TeV. Which means that when suggesting an initial value to the fitting code, you would want
to use **3** rather than **3000** as the mean for a gaussian peak on top of the background. 

In the process of getting this right, I produced about a million of these graphs

![image](https://github.com/H4rtland/masters/blob/master/week8/imgs/output_qstar_bad.png "")

And after realising my mistake eventually ended up with one of these.

![image](https://github.com/H4rtland/masters/blob/master/week8/imgs/output_qstar_good.png "")

The gaussian peak is slightly mismatched on the higher energy tail, as the qstar distribution
has more of a sharp falloff on this edge, rather than gauss-like. 
