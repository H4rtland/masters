### Week 4
###### November 13th-19th 2017

#### Translating FitMass.C to Python

Fitting the parameters of a function to a curve involves a trial and error process
of slowly changing things until it eventually works - and so does converting a ROOT
program in C++ to a PyROOT script.

Luckily, PyROOT can load compiled ROOT macros, so I didn't have to even touch IABStyle.C.
I also loaded a compiled version of the MyMassSpectrum fitting function straight from the
C++ version, because an equivalent class written in Python caused this error in the GaussIntegrator

    Error in <ROOT::Math::ROOT::Math::GausIntegratorOneDim>: A function must be set first!

even when I had clearly just set the function. Replacing this with the compiled C++ version worked.
This means that
```
$ root -l
root [0] .L IABStyle.C+g
root [1] .L FitMass.C+g
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
converts your list of ten 0s to an array of doubles.
In other cases you're allowed to not convert things. For example
```python
ierflg = ROOT.Long(0)
self.gMinuit.mnparm(0, "p1", 5e-6, 1e-7, 0, 0, ierflg)
```
ierflg did need to be converted, the other numbers didn't.
Based on the error message it's because ierflg is then used to pass by reference.
