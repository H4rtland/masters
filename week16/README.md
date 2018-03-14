## Week 13
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



