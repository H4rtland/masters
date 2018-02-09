## Week 4
###### November 13th-19th 2017

### Translating FitMass.cpp to Python

Using code in cross_section_example.

Fitting the parameters of a function to a curve involves a trial and error process
of slowly changing things until it eventually works - and so does converting a ROOT
program in C++ to a PyROOT script.

Luckily, PyROOT can load compiled ROOT macros, so I didn't have to even touch IABStyle.cpp.
I also loaded a compiled version of the MyMassSpectrum fitting function straight from the
C++ version, because an equivalent class written in Python caused this error in the GaussIntegrator

    Error in <ROOT::Math::ROOT::Math::GausIntegratorOneDim>: A function must be set first!

even when I had clearly just set the function. Replacing this with the compiled C++ version worked.
This means that
```
$ root -l
root [0] .L IABStyle.cpp+g
root [1] .L FitMass.cpp+g
```
needs to be run before the Python code can work. At this point is there any reason to
even use the Python version? No, but it's too late to turn back now.

Other things which took a while to get right included:

Returning the value of chisq from Fitfcn had to be changed from
```c++
fcnVal = chisq;
```
to
```python
fcnVal[0] = chisq
```
because how should we get the value that this function should return? No, let's not `return` it,
let's pass in a value for it to modify by reference. Great.

Also, any time a ROOT function complains about you not giving it the correct argument types,
you probably have a list that needs converting explicitly, i.e
```python
import array
arglist = array("d", [0,]*10)
arglist[0] = ROOT.Double(1)
```
converts your list of ten 0s to an array of doubles and changes the first value to a 1.
In other cases you're allowed to not convert things. For example
```python
ierflg = ROOT.Long(0)
self.gMinuit.mnparm(0, "p1", 5e-6, 1e-7, 0, 0, ierflg)
```
ierflg did need to be converted, the other numbers didn't.
Based on the error message it's because ierflg is then used to pass by reference.

Well, in the end we get back the exact same plot that is produced by the C++ code.

![image](https://github.com/H4rtland/masters/blob/master/week04/cross_section_example/output.png "")

### Fitting actual data

Using code in cross_section_data.

fit_mass.py in cross_section_data loads data from a histogram in 
Fourth_Year_Data/mjj_data15_13TeV_00276262_physics_Main_total_final.root.
Other than that, it's almost exactly the same as the example file.
As is loads the data it scales the x axis values by a factor of 1e-3 so they
are between 1 and 10 rather than 1000 to 10000, this is so that the initial fitting
parameters used in the example still work. The error values are also changed, so that instead of
a consistent 5% error, it uses sqrt(N) (where N is the number of events in a bin). 

![image](https://github.com/H4rtland/masters/blob/master/week04/cross_section_data/output.png "")

FitMass.cpp is renamed to FitFunction.cpp and is stripped of everything except
the MyMassSpectrum class which is needed for the Python code to work.
Of course, once again we need to run
```
$ root -l
root [0] .L IABStyle.cpp+g
root [1] .L FitFunction.cpp+g
```
before the python code will work.

#### Resources

TMinuit fitting  
https://pprc.qmul.ac.uk/~bevan/yeti/fitting.pdf
