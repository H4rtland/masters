### Week 3
###### November 6th-12th 2017

#### 1 Fitting to a constant

![image](https://github.com/H4rtland/masters/blob/master/week3/example1/Fit_Example_1.png "")

#### 2 Fitting to a Gaussian

![image](https://github.com/H4rtland/masters/blob/master/week3/example2/Fit_Example_2.png "")

#### 3 Fitting to a wide Gaussian

![image](https://github.com/H4rtland/masters/blob/master/week3/example3/Fit_Example_3.png "")

#### 4 Fitting to a Gaussian on a constant background

![image](https://github.com/H4rtland/masters/blob/master/week3/example4/Fit_Example_4.png "")

![image](https://github.com/H4rtland/masters/blob/master/week3/example4/Fit_Example_4_myfit.png "")

#### 5 Gaussian on a constant background II

![image](https://github.com/H4rtland/masters/blob/master/week3/example5/Fit_Example_5.png "")

#### 9 Guassian on a linear background

![image](https://github.com/H4rtland/masters/blob/master/week3/example9/Fit_Example_9.png "")

![image](https://github.com/H4rtland/masters/blob/master/week3/example9/Fit_Example_9_2.png "")


#### 10 Gaussian on a linear background using separate functions

![image](https://github.com/H4rtland/masters/blob/master/week3/example10/Fit_Example_10.png "")

![image](https://github.com/H4rtland/masters/blob/master/week3/example10/Fit_Example_10_2.png "")


#### Notes

When plotting on a remote machine, adding the line

```python
gROOT.SetBatch(True)
```

means that a window won't be opened when drawing.
Opening/drawing/closing takes quite a while since it's being done remotely, so just writing to a file is quicker.
And my window manager insists on changing the window size which causes the drawn file to spill over the edges of the actual image dimensions.


#### Cross section

I didn't rewrite this example to Python. There's quite a lot of c++ already there and it didn't seem worth redoing it all.
