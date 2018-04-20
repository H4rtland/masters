## Week 17
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

The q\* plot seems to have changed slightly compared to the week 13 version, but since
I've been having so much trouble getting the code to even run I don't want to risk
breaking it further trying to get back to what I had then. And I am slightly concerned about
the shape of the 2000 and 2500 GeV distributions in plt61672. The 2000 is zeroed at a big chunk of
masses near 2400 GeV, and the 2500 GeV and 3500 GeV distributions have a big peak at the left
that doesn't exist in the 3000 GeV distribution. I wouldn't be surprised if this is what was
contributing to the odd shape I have on the left of my q\* brazil plot where it isn't very smooth.
This irregularity has existed since week 13, now that I look back at it though. 

While writing the report I've just added a few lines to the brazil plot code to show the
effect of including the 3.2% uncertainty on the luminosity. For the QBH 61673 run the difference
is not as much as I was thinking it would be.

```
Without luminosity uncertainty
Mass    Mean    low2s   low1s   high1s  high2s
4000    61.96   42.50   50.50   74.50   93.50
5000    25.48   16.30   19.70   31.30   41.10
5500    18.16   11.30   13.70   22.70   30.50
6000    12.90   7.85    9.55    16.35   22.05
6500    9.70    5.73    7.13    12.43   16.82
7000    7.27    4.53    5.33    9.23    12.63
7500    5.85    3.93    4.33    7.33    10.13
8000    4.84    3.62    3.83    5.93    8.03
8500    4.24    3.52    3.62    5.03    6.73
9000    3.92    3.43    3.52    4.43    5.93
9500    3.71    3.33    3.43    4.03    5.23
10000   3.62    3.33    3.33    3.93    5.13
```

```
With luminosity uncertainty
Mass    Mean    low2s   low1s   high1s  high2s
4000    62.03   42.50   49.50   74.50   93.50
5000    25.50   16.30   19.70   31.30   41.10
5500    18.18   11.10   13.70   22.70   30.30
6000    12.91   7.75    9.55    16.35   22.25
6500    9.70    5.68    7.08    12.43   16.88
7000    7.27    4.43    5.33    9.18    12.68
7500    5.85    3.83    4.33    7.38    10.23
8000    4.84    3.58    3.83    5.93    7.98
8500    4.25    3.38    3.58    5.03    6.73
9000    3.93    3.27    3.43    4.43    5.98
9500    3.71    3.18    3.33    4.08    5.28
10000   3.62    3.18    3.27    3.88    5.03
```

And for q\* 61672 the story isn't much different. There doesn't seem to be any consistency
in whether the mean/sigmas are moving up or down between the different masses. It should be noted
that repeat runs of the brazil plot code with the uncertainty enabled produce the exact
same results. Here's the q\*:

```
Without luminosity uncertainty
Mass    Mean    low2s   low1s   high1s  high2s
2000    2212.56 1352.50 1647.50 2757.50 4087.50
2500    1853.79 947.50  1212.50 2597.50 3502.50
3000    1620.89 747.50  1072.50 2142.50 2687.50
3500    591.56  307.50  392.50  822.50  1112.50
4000    240.13  143.50  178.50  294.50  448.50
4500    118.61  74.50   90.50   146.50  193.50
5000    66.57   42.10   51.30   82.10   107.50
5500    43.42   27.50   33.30   53.50   71.50
6000    31.10   19.35   23.45   38.75   51.25
6500    24.56   15.23   18.52   30.62   40.62
7000    20.51   12.63   15.33   25.73   34.33
```

```
With luminosity uncertainty
Mass    Mean    low2s   low1s   high1s  high2s
2000    2214.37 1357.50 1642.50 2772.50 4052.50
2500    1855.39 937.50  1207.50 2602.50 3482.50
3000    1622.03 747.50  1072.50 2142.50 2697.50
3500    592.10  307.50  392.50  812.50  1112.50
4000    240.41  141.50  176.50  294.50  450.50
4500    118.72  73.50   90.50   147.50  193.50
5000    66.63   41.70   51.10   82.30   107.50
5500    43.46   27.30   33.10   53.50   71.70
6000    31.13   19.15   23.45   38.95   51.55
6500    24.58   15.23   18.43   30.77   40.88
7000    20.53   12.48   15.28   25.77   34.33
```

On disturbing thing I noticed was that when I printed out the randomly generated luminosity for
every 1000th limits, I saw repetitions.

```
Lim  Luminosity    37*Lim/Luminosity
92.6 36.8182445354 93.0571254344
72.2 37.3276112213 71.5663261751
49.2 38.7948886979 46.9237072486
63.8 36.5917782587 64.5117595355
75.6 36.0256170587 77.644749164
43.6 36.8182445354 43.8152340058
44.8 37.3276112213 44.4068062693
51.2 38.7948886979 48.8311750229
51.8 36.5917782587 52.3778862686
48.4 36.0256170587 49.7090722161
30.7 36.8182445354 30.8515523848
47.3 37.3276112213 46.8848646549
20.6 38.7948886979 19.6469180756
33.8 36.5917782587 34.1770763683
22.9 36.0256170587 23.5193750775
```

Notice that the 36.818 comes back on the 6th line. That's 5000 limits apart, but it's still
a repetition.

Changing from using the TRandom class to TRandom1 has fixed the repetition issue. However,
the sigmas are still a little odd.

```
With luminosity uncertainty
Mass    Mean    low2s   low1s   high1s  high2s
2000    2214.59 1352.50 1642.50 2752.50 4077.50
2500    1856.64 942.50  1207.50 2592.50 3532.50
3000    1623.13 737.50  1067.50 2137.50 2692.50
3500    591.81  307.50  392.50  817.50  1117.50
4000    240.63  142.50  177.50  294.50  450.50
4500    118.75  74.50   89.50   147.50  192.50
5000    66.67   41.90   51.10   82.50   107.10
5500    43.45   27.30   33.10   53.30   71.70
6000    31.14   19.15   23.45   38.85   51.65
6500    24.59   15.13   18.43   30.57   41.12
7000    20.53   12.58   15.33   25.82   34.23
```

I expected that the high 1sigma and 2sigma would move up compared to the no uncertainty case.
Because the distribution should be smeared out, and there are more limits that can move
up than there are that can move down over at the high mass end.

Also while I'm editing this file I'll include an update for the W' brazil plot. In the one
I have above it turned out that I was using an old data line which included the 2017 data,
which is why it is so far off the expected line. This is the new one:

![image](https://github.com/H4rtland/masters/blob/master/week17/imgs/brazil-61674-2.png "")

