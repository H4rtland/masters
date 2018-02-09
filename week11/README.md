## Week 11
###### February 5th-11th 2018

### Distribution of 95% Confidence Level Limit

The next step is to run many of these tests and plot a distribution of the 95% confidence
level limits. Starting off with generating 300 limits and plotting a histogram, we get this:

![image](https://github.com/H4rtland/masters/blob/master/week11/imgs/cl_dist_1.png "")

We can clearly see the beginnings of a gaussian distribution here, but it still isn't very well
defined. (Looking at this later on, I think I can say for sure that the spiky nature of this
histogram is due to the likelihood loop increasing the number of events by 25 each time,
and the histogram plotting with bin widths of 15, meaning that it's impossible for some bins
to ever have data in).

The problem now is the time factor. Just generating these 300 data points took this long

```
real    12m55.262s
user    12m29.835s
sys     1m13.574s
```

We need to generate much more data than this to get a good distribution, and *then* we are going
to have to generate one of these for each mass data set that has been simulated for the q\*.
This is the right time to start submitting this work to the physics department batch job service.
This is a particularly suitable workload for such a servie, because it is "embarassingly
parellel" - each random generation and subsequent analysis has no dependence on any of the others,
so they can be run completely separetely. Running 10 different jobs on the batch system will
generate 10 times as much data in the same time as one job.

The jobs are submitted as JDL files. Here's what the one I'm using looks like.

```
executable     = job_limit.sh
universe       = vanilla
arguments      = "$(CLUSTER).$(Process)"
output         = logs/std-$(CLUSTER).$(Process).out
error          = logs/std-$(CLUSTER).$(Process).err
log            = logs/std-$(CLUSTER).$(Process).log
request_memory = 100
concurrency_limits = myusername:100
queue 1
```

The two parts of the job ID, $(CLUSTER) and $(Process), are passed as arguments to the bash script.
That script then passes that argument on to python, so that it can put together a unique
name for an output file to write to.

The job_limit.sh file contains some setup for ROOT, and a line to activate the python
virtualenv I'm using, and then executes the python script.

```bash
#! /bin/bash -f

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

WORKDIR=/home/atlas/thartland/masters/week11
cd ${WORKDIR}

lsetup root

source /home/atlas/thartland/venvs/root-py2/bin/activate

python limit_dist.py "$1"
```

I've now renamed the python script to limit_dist.py, although I might change it again if I think
of a better name. I've also deleted a lot of the old code that wasn't being used any more. The
python code that is being run now boils down to this:

```python
with open("results/job-{0}.txt".format(sys.argv[1]), "w") as out_file:
    for i in range(0, 10):
        out_file.write("{0}\n".format(fit_significance(0, plot=False)))
```

Where sys.argv[1] is the cluster/process argument passed all the way from the job description.
It could also be changed to take the number of iterations to run from the arguments as well.

Now that I've tested submitting a single job with only 10 iterations of the 95% C.L limit test,
let's scale up: 10 jobs running 250 iterations each:

```
[thartland@lapa week11]$ condor_submit job.jdl 
Submitting job(s)..........
10 job(s) submitted to cluster 50599.
[thartland@lapa week11]$ condor_q thartland


-- Schedd: lapa.lancs.ac.uk : <148.88.40.17:9618?...
 ID      OWNER            SUBMITTED     RUN_TIME ST PRI SIZE CMD               
50599.0   thartland       2/8  23:47   0+00:00:09 R  0   0.0  job_limit.sh 50599
50599.1   thartland       2/8  23:47   0+00:00:09 R  0   0.0  job_limit.sh 50599
50599.2   thartland       2/8  23:47   0+00:00:09 R  0   0.0  job_limit.sh 50599
50599.3   thartland       2/8  23:47   0+00:00:09 R  0   0.0  job_limit.sh 50599
50599.4   thartland       2/8  23:47   0+00:00:09 R  0   0.0  job_limit.sh 50599
50599.5   thartland       2/8  23:47   0+00:00:09 R  0   0.0  job_limit.sh 50599
50599.6   thartland       2/8  23:47   0+00:00:09 R  0   0.0  job_limit.sh 50599
50599.7   thartland       2/8  23:47   0+00:00:09 R  0   0.0  job_limit.sh 50599
50599.8   thartland       2/8  23:47   0+00:00:09 R  0   0.0  job_limit.sh 50599
50599.9   thartland       2/8  23:47   0+00:00:09 R  0   0.0  job_limit.sh 50599

10 jobs; 0 completed, 0 removed, 0 idle, 10 running, 0 held, 0 suspended
```

And now we have a folder full of output files:

```
[thartland@lapa week11]$ ls results
job-50599.0.txt  job-50599.2.txt  job-50599.4.txt  job-50599.6.txt  job-50599.8.txt
job-50599.1.txt  job-50599.3.txt  job-50599.5.txt  job-50599.7.txt  job-50599.9.txt
```

which can be joined together

```
[thartland@lapa week11]$ cat results/* > results-all.txt
```

However, something doesn't seem right.

```
[thartland@lapa week11]$ wc -l results-all.txt 
2268 results-all.txt
```

Only 2268 lines? I was expecting 10\*250 = 2500. Let's investigate.

```
[thartland@lapa week11]$ cd logs
[thartland@lapa logs]$ ls -lh | grep err
-rw-rw-r-- 1 thartland thartland  117 Feb  8 23:48 std-50599.0.err
-rw-rw-r-- 1 thartland thartland  117 Feb  8 23:48 std-50599.1.err
-rw-rw-r-- 1 thartland thartland 140K Feb  8 23:52 std-50599.2.err
-rw-rw-r-- 1 thartland thartland 140K Feb  8 23:49 std-50599.3.err
-rw-rw-r-- 1 thartland thartland 141K Feb  8 23:55 std-50599.4.err
-rw-rw-r-- 1 thartland thartland  117 Feb  8 23:48 std-50599.5.err
-rw-rw-r-- 1 thartland thartland  117 Feb  8 23:48 std-50599.6.err
-rw-rw-r-- 1 thartland thartland  117 Feb  8 23:48 std-50599.7.err
-rw-rw-r-- 1 thartland thartland  117 Feb  8 23:48 std-50599.8.err
-rw-rw-r-- 1 thartland thartland 103K Feb  8 23:53 std-50599.9.err
```

Yep, looks like we definitely had some errors somewhere. 

...

You know, I thought these error files were going to be helpful, but they're actually just
my worst nightmare. The first abnormally large file std-50599.2.err is literally just 140KB
of "GausIntegrator:0: RuntimeWarning: Failed to reach the desired tolerance".

The second is slightly more helpful. Right at the very end of the file there's an actual error.

```
Traceback (most recent call last):
  File "limit_dist.py", line 326, in <module>
    plot_95pc_confidence_dist()
  File "limit_dist.py", line 322, in plot_95pc_confidence_dist
    out_file.write("{0}\n".format(fit_significance(0, plot=False)))
  File "limit_dist.py", line 268, in fit_significance
    ycumulative = [yval/max(ycumulative) for yval in ycumulative]
ZeroDivisionError: integer division or modulo by zero
```

I really don't know how the maximum value of ycumulative can be 0, but I'll take a look a this
later, for now let's check the other error logs.

Yep, file 3 is also a divide by 0 error, and file 9 is just more GausIntegrator warnings only.

Still, we do have 2268 lines of actual results, so I'll plot those before I go back to fix things.

![image](https://github.com/H4rtland/masters/blob/master/week11/imgs/cl_dist_2.png "")

This is much better! Each job was only running 250 trials, which takes about 10 minutes, so there's
still plenty of space to scale into, both for the number of trials per job and the number of jobs.
