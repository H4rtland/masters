## Week 8
###### January 22nd-28th 2018

### Statistics of signal injection test

Firstly I'm experimenting with enabling/disabling the final fitting stage which
unlocks all parameters. Disabling it cuts the time taken per trial by about half
but I'm not sure how to judge how much it affects the accuracy of the fit.

Looking at the output results, disabling the last stage reduces the spread of results,
and brings the average closer to the input value. I'll leave it disabled for now and once
I have a histogram of the results distribution I'll enable it again and hopefully it will
be easier to see what's going on.

```python
distribution = TH1D("dist", "dist", 60, 3700, 4300)
with open("results.txt", "w") as out_file:
    ....

canvas = TCanvas("Canvas", "Distribution Canvas", 0, 0, 650, 450)
distribution.Draw()
canvas.SaveAs("dist.png")
```

This is the first look at the distribution for 200 trials with the final fitting stage disabled:

![image](https://github.com/H4rtland/masters/blob/master/week9/imgs/dist1.png "")

And with the final fitting stage enabled:

![image](https://github.com/H4rtland/masters/blob/master/week9/imgs/dist2.png "")

The RMS is reduced by a factor half with the last stage disabled. The second distribution
seems to be more gaussian so I'll keep the code in this state for now.
