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

![image](https://github.com/H4rtland/masters/blob/master/week12/imgs/95pcCL_dist_51309.png "")

This distribution was produced before making the changes in the above section, which is why
there is still a massive spike at 2380.

The mean of the dstribution now looks to be at ~1200, whereas last week it was ~800.
The backgrounds should be almost identical, so I'm not sure what's causing this.

These are some samples of the histogram bin contents and the theoretical value I was calculating
before (these are NOT the randomly generated values, those are based on these numbers)

```
hist:1033970.12239  mine:1016022.10606
hist:863719.349551  mine:869095.677677
hist:749091.2556    mine:744507.498295
hist:630876.729938  mine:638683.13645
hist:548767.728998  mine:548649.867284
hist:473323.678317  mine:470927.486618
........
hist:91052.6108567  mine:92194.6314089
hist:79596.9521148  mine:79718.0459191
hist:69383.0570701  mine:68892.3441672
hist:58658.4660953  mine:59601.8061133
hist:51094.1180384  mine:51617.953889
hist:44391.2921914  mine:44679.3038759
........
hist:10454.669244   mine:10501.3551099
hist:9088.96027485  mine:9070.11858829
hist:7858.29288964  mine:7830.75796039
hist:6784.19914512  mine:6758.01662113
hist:5863.79233368  mine:5829.88246811
hist:5039.00987776  mine:5027.18662084
```

The values are close enough that I wouldn't think they could cause such a huge change in the
95% limit distribution. Also neither side is always higher than the other, it seems to be random
which is higher and which is lower, which I would think means that the limit shouldn't
be skewed entirely in one direction by the change of data. Although at about the 10,000 events
area, which is approximately where our peak is getting added on to, the Pythia data does seem to
be slightly lower in most of the bins, which would mean that a given size peak would be
comparatively less likely to be able to describe the data. Though surely this would move the limit
down rather than up? Well, I'll keep going with these values for now and it'll probably be alright.

With the fixes in place for the non converging fits, the mean of the distribution goes to almost
exactly 1200, as I guessed earlier.

![image](https://github.com/H4rtland/masters/blob/master/week12/imgs/95pcCL_dist_51310.png "")

This will do for now. Since the aim is to produce a brazil plot, we're now going to need to
extend the batch system to also run jobs for q\* data at other masses. Ideally I'd like to have
just one job to submit that then organises running the entire thing. I thought about separating
by the different $(Process) numbers so that process 0 runs with one file, process 1 runs another,
etc. If there were 5 files to test with, 10 jobs would use each of the files twice, so it would
be separating by ID mod 5. But then I'm sure I'll run into some issues with this where
I might want to only run one specific file.

Ah, I've found what I need. I had looked at the Queue Arguments From syntax for htcondor jobs,
but that would mean duplicating lines to run multiple of the same arguments.

The best I'm going to get is something like this:

```
executable     = job_limit.sh
universe       = vanilla
arguments      = "$(CLUSTER) $(CLUSTER).$(Process) $(mass)"
output         = logs/std-$(CLUSTER).$(Process).out
error          = logs/std-$(CLUSTER).$(Process).err
log            = logs/std-$(CLUSTER).$(Process).log
request_memory = 100
concurrency_limits = thartland:50


mass = 1000
queue 5

... other masses ...

mass = 7000
queue 5
```

Which seems flexible enough for my needs. The mass is now passed as the third argument
to each script. Results are also separated into subdirectories based on this value.

Distributions at each mass point can be found in the directory plt51318 above.

Starting with the distribution plotting code, I then modified it to create a brazil plot,
which combines the means and root-mean-squares of each distribution into one plot.

I had to battle with ROOT a bit to get it to plot what I want, but the turning point was
finding the TMultiGraph class, which allowed me to draw the yellow and green bands of the brazil
plot at the same time. Before that I either had the background of one plot drawing
over the band on the other, or I ended up with a completely blank output.

Then I added in the dotted line for the mean values, and fiddled around with the styling a bit,
and finally arrived at the end result!

![image](https://github.com/H4rtland/masters/blob/master/week12/imgs/brazil-51318.png "")

This is for a 95% confidence level limit distribution containing 2000 entries at each
mass point. The mean and RMS of the limit of number of events is divided by 37000 to get
the limit on the cross section in units of pb, as the data set is 37fb^-1. 

For reference, the ATLAS q\* brazil plot looks like this.

![image](https://github.com/H4rtland/masters/blob/master/week12/imgs/atlas_qstar.png "")

