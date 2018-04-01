## Week 16
###### March 19th-25th 2018

### Continuation

It turns out that the 2017 data is not compatible with the 2016 data at all, so I won't be
using it for actual results. I will however keep some plots with the scaled background
for the expected limits, to show some "here's what the limits will look like with the next data"
plots.

To start finishing up on the plotting I've tried plotting the WStar data, but the bins in the 
monte-carlo simulation histogram do not match the position of the bins in the WStar peak
histograms. I am not sure if I will be trying to fix this or just ignoring them to work on
some other things instead.

For my own sake here is a list of things that still need to be done.

* Make updated brazil plots for q\* / QBH / W' using the latest brazil plot code.
* Not sure if I want to generate new data for those or not.
* Make scaled plots to show expected limits for old+new data.
* Maybe revisit WStar
* Actually write the report.

Since I haven't included them here yet, here are the updated brazil plots with
proper legends / other decoration.

![image](https://github.com/H4rtland/masters/blob/master/week17/imgs/brazil-55841.png "")

Observed mass limit: 6731 GeV  
Observed cross section limit: 0.0003286 pb  
Expected mass limit: 6549 GeV  
Expected cross section limit: 0.0004807 pb  

![image](https://github.com/H4rtland/masters/blob/master/week17/imgs/brazil-55842.png "")

Observed mass limit: 9161 GeV  
Observed cross section limit: 5.726e-05 pb  
Expected mass limit: 9152 GeV  
Expected cross section limit: 5.892e-05 pb  

![image](https://github.com/H4rtland/masters/blob/master/week17/imgs/brazil-55843.png "")

Observed mass limit: 3843 GeV  
Observed cross section limit: 0.007612 pb  
Expected mass limit: 4030 GeV  
Expected cross section limit: 0.005265 pb  

These will need to be updated after I switch back to using 2016 data only.

Well I set the new jobs to run yesterday, and some of the highest mass ones are still running
almost 24 hours later. When I check the logs files, I see that most of the loops
are still only taking ~3-4 seconds, however some of them are taking much longer.

```
1732   FUNCTION VALUE DOES NOT SEEM TO DEPEND ON ANY OF THE 4 VARIABLE PARAMETERS.
1733           VERIFY THAT STEP SIZES ARE BIG ENOUGH AND CHECK FCN LOGIC.
1734  *******************************************************************************
1735  *******************************************************************************
1736   FUNCTION VALUE DOES NOT SEEM TO DEPEND ON ANY OF THE 4 VARIABLE PARAMETERS.
1737           VERIFY THAT STEP SIZES ARE BIG ENOUGH AND CHECK FCN LOGIC.
1738  *******************************************************************************
1739  *******************************************************************************
1740   FUNCTION VALUE DOES NOT SEEM TO DEPEND ON ANY OF THE 4 VARIABLE PARAMETERS.
1741           VERIFY THAT STEP SIZES ARE BIG ENOUGH AND CHECK FCN LOGIC.
1742  *******************************************************************************
1743  *******************************************************************************
1744 Iteration 61637.50.i740 max(ycumulative)=0
1745 Iteration 740, limit = None, time = 17431.82
```

Yep, that's almost 5 hours on a single loop. Most of the loops that get this big error message
fail quickly, only taking 1-2 seconds, but there are just a few that are taking hours.
I assume that most of the time is taken up by the root fitting, so I'm not sure if there's
any way that I can intervene halfway through once it's clearly going to take longer than usual.

In the limit_dist.py I copied for the W\* data I changed the default fitting parameters to account
for the change back to 37fb^-1 of data, but I forgot to in the file for q\* / QBH / W', so that
might be the reason. I'll run the whole thing again now I've changed those parameters back
and see if this keeps happening. I'll cancel the currently running jobs as well.

Ok, turns out I had changed back the default parameters and I was looking at the wrong file earlier.
In the many hours since then all I've managed to do is make things worse. I still can't get the
fitting at 7000 GeV to work all of the time, and half of the time at 3000 GeV the fit fails to
converge. This *never* used to happen. Oh, looks like I've fixed that actually.

Alright, without me really doing anything, everything has just fixed itself. I'll now run a longer
test for the 7000 GeV mass q\* to check that it is in fact working and I wasn't just lucky
for the 50 iterations I ran. But compared to earlier where it was crashing by the first couple
of iterations, this is an improvement.

That didn't fix it, but I think I have fixed it now. I made some changes including switching
some of the python math.log calls for TMath.Log calls. This fixed at least one error I was
getting (although I don't think it was causing the mass failures). I also separated the first
fitting stage into two, two fit the first two parameters separately, and set some bounding
values for the first parameter. Things seem to be going smoothly now, and I've got generated
limits for all three particles. I'm not including W\* yet because I don't have compatible
peaks/backgrounds still.

And so, these are the new brazil plots for 37fb^-1.

![image](https://github.com/H4rtland/masters/blob/master/week17/imgs/brazil-61672.png "")

![image](https://github.com/H4rtland/masters/blob/master/week17/imgs/brazil-61673.png "")

![image](https://github.com/H4rtland/masters/blob/master/week17/imgs/brazil-61674.png "")
