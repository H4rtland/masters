## Week 16
###### March 12th-18th 2018

### New data

We now have a new data set to add to our current one. The new data is 32 fb^-1.

This is the result of performing a per-bin ratio between the new / old data.

![image](https://github.com/H4rtland/masters/blob/master/week16/imgs/data_cmp.png "")

Errors are added in quadrature and bins which do not have data in both the new and old
histograms are excluded. At the lowest mass scale the ratio starts out as ~1.15 (37/32)
but drops down below that rather than staying level. This means that there is a noticable effect
due to the triggers having a higher p_T threshold for this data.

Still, we can proceed to add this data to our current data for a total of 69fb^-1 of data.
The smooth background theory that is used to generate random distributions can also
be scaled by 69/37 to get it to match the new amount of data.

```python
hist.Scale(69/37)
```

Based on the week13 plots for job 51329, the mean 95% C.L limit for M=3000 GeV is 1195 for 2500
trials. This corresponds to a cross section limit of 1195/37000 = 0.0323 which is what is
plotted on the brazil plot. Running limit_dist.py again, for the new scaled background
over 500 trials gives a 95% limit mean of 1864.2, and a cross section limit of
1864.2/69000 = 0.0270. This is comparable to, and slightly lower than, the original
cross section limit which is as expected. The next step will be to generate a complete
results set for all mass points using the new data. 

Before that, I have run limit_dist.py manually with the 2000 GeV q\* data, to check that
the peak limit testing was not being cut off. The original value was to stop at 5000 events
in the peak, and this has now been increased to 10000. In almost all cases this limitation
on the number of events was never being reached anyway, and even now at 2000 GeV the average limit
still seems to be in the mid 2000s.

I also took this chance to alter the initial parameters of the fit. The fitting is slightly
faster after changing the parameters, and I am now sure that they work for the new data.

![image](https://github.com/H4rtland/masters/blob/master/week16/imgs/plot-abc1.i1-2000-hist.png "")

I have also slightly changed the events step based on the mass, to account for the limit
distribution peaks being further to the right and slightly wider. The new conditions are

```
default   --> step = 5
M >= 4000 --> step = 1
M >= 5000 --> step = 0.2
M >= 6000 --> step = 0.1
M >= 6500 --> step = 0.05
```

While making these changes I was checking the typical limits for each q\* mass and also
keeping an eye on how long each iteration was taking. I have added in some code to write out
to a file how long each iteration takes along with what the limit was for that loop, and I will
see if there is anything interesting in that data after I have run all the batch jobs.

First: the per-iteration time data. 

![image](https://github.com/H4rtland/masters/blob/master/week16/imgs/times.png "")

Each histogram plots iteration time (in seconds) on the x axis and frequency on the y axis.
There is some kind of clear separation going on here, which I think is probably a result
of how well the fitting stage performs. Why the times are *so* grouped up, I'm not sure.
The limits are distributed as a gaussian as we have already seen, so they are unlikely to
be causing grouping like this for the iteration times (although they may be the cause of the
approximately gaussian shape around each of the peaks in the time distributions).

Only the loops where a limit was found sucessfully are included in these histograms,
so the separation is not due to some "error"/"no error" difference. Following the path through
the code that produces an actual value for a limit, there are no code branches that would
make some loops take significantly longer, i.e if some loops were generating plots
(this is currently disabled). I'll see if there are any parameters I can get out of TMinuit
that I might be able to link to the data we're seeing here.

Second item on the agenda was the data I had generated at the same time as the time plots.
I didn't actually do anything with that data and instead I have a more recent set to work with.

I changed the code around so that I could run it for the different q\* / QBH / WPrime
simulated peaks just by changing the job file. These are now job_qstar.jdl, job_qbh.jdl and
job_wprime.jdl.

I have also added some lines to the brazil plot code to calculate the intersection of the
black data line and the blue theory line. I started this last Friday and spent an hour trying
to get it to work, but every time the intersection point was offset to the right of where it
should have been. Then on Sunday night while doing some completely unrelated work I glanced
at the piece of paper I had rearranged the straight line equations on the find the intersect,
and had a sudden realisation of "they're only straight lines on the log plot!". So I've now
fixed that.

And so, here are the brazil plots for excited quarks, quantum black holes and W primes,
using the newer, larger data set:

![image](https://github.com/H4rtland/masters/blob/master/week16/imgs/brazil-55841.png "")

![image](https://github.com/H4rtland/masters/blob/master/week16/imgs/brazil-55842.png "")

![image](https://github.com/H4rtland/masters/blob/master/week16/imgs/brazil-55843.png "")

I do have some doubts about how exactly the intersect should work. The straight lines are
simply lines I have drawn on between the points. The points are all that the data
actually gives us, and there is no real reason that there should be straight lines joining
them. It's probably a good enough approximation though, and certainly I don't want to
have to code anything more complex that what I have already.
