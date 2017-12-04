## Week 6
###### November 27th - December 3rd 2017

### Maximum likelihood fitting

Maximum likelihood is an alternative method to chi^2 fitting.
It is in general equivalent to chi^2 for bins with large numbers of events,
but handles bins with few events more accurately. This is especially important
in this project, where we will be dealing with rare decay processes which may only
produce up to tens of events.

Mathematically, the log of the likelihood, L, is given by this equation.

![image](https://github.com/H4rtland/masters/blob/master/week6/imgs/eqn1.png "")

This is the extended log-likelihood function.
We want to *maximise* this value. Instead, we take the negative of this sum
and let the already established minimisation functions do their work.
The values of n_i are the values from the data, and the v_i are the values
predicted by the model for a given set of parameters. v_tot is the sum(v_i). 
Also, it seems to be fine to just ignore the log function acting on L and
minimise the entire left side of the equation. 

This took some effort to get working. To get it going, there were a few
cases that needed to be account for. First, the case where v_i <= 0.
All bins for which the value of the model prediction is less than 0 must
be discarded, as the log function is undefined for negative input.
Further to that, considering a negative number of events in a bin
would be meaningless anyway.
Secondly, the format of the data being worked with included empty bins
to the left of the data. This is in the range where the model predictions
are on the order of millions of events. Trying to fit these together produced
an incorrect (yet amusing) fit line.

These excluded cases are incorporated into the code like so

```python
if model_val <= 0 or (self.data[i] == 0 and self.xmins[i] < 2):
    continue
```

This is in the loop of a new fit function, defined just underneath the chi^2 version,
just above the part where it calculates and adds the sum term for bin [i]. I called this
summation variable `likelihood`, but in the extended log-likelihood method, I should
actually also be subtracting the v_i from this term. Instead, I track the total v_tot
and subtract it at the end to match the form of the above equation.

```python
likelihood += self.data[i] * math.log(model_val)
```

Finally, at the end of the function, we send back the negative of the likelihood.

```python
fcnVal[0] = 2*(model_total-likelihood)
```
The factor of two here is a correction to get the values of the errors
in the parameters reported by Minuit right. The factor of 2 also appears
in a similar fitting method, which produces a chi^2 for a poisson distributed n_i.

![image](https://github.com/H4rtland/masters/blob/master/week6/imgs/eqn2.png "")

This is not necessary to be used for fitting, but can be used to test the goodness
of a fit in comparison to a regular chi^2 calculation.

The final plot produced by the maximum log-likelihood method looks almost exactly the same
as the plots from previous weeks (as you would hope).

![image](https://github.com/H4rtland/masters/blob/master/week6/imgs/log_likelihood_output.png "")

