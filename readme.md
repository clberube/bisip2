# BISIP
[![Documentation Status](https://readthedocs.org/projects/bisip/badge/?version=latest)](https://bisip.readthedocs.io/en/latest/?badge=latest)

### This is the development repository for BISIP2, the successor of BISIP: https://github.com/clberube/BISIP. BISIP is being re-written with a powerful ensemble MCMC sampler, better code practice and improved documentation.


### Requirements
- Python 3 (BISIP is developed on Python 3.7)  
- emcee (https://emcee.readthedocs.io/en/stable/)
- numpy (https://numpy.org/)
- matplotlib (https://matplotlib.org/)


### Documentation
Visit https://bisip.readthedocs.io/en/latest/ to consult the full documentation including API docs, tutorials and examples.

### Installation
Clone this repository to your computer. Then navigate to the bisip directory. Finally run the setup.py script with Python.

```
git clone https://github.com/clberube/bisip2
cd bisip2
python setup.py install -f
```

### Quickstart
Import BISIP in your Python scripts as follows:

```python
from bisip import PolynomialDecomposition

# Define a Polynomial Decomposition model with
# a 4th order approximation and c-exponent equal to 1 (Debye)
# The simulation will run for 500 steps with 32 walkers
# exploring the Debye Decomposition parameter space
model = PolynomialDecomposition(nwalkers=32,  # number of walkers
                                nsteps=500,  # number of MCMC steps
                                poly_deg=4,  # 4th order polynomial
                                c_exp=1.0,  # debye decomposition
                                )

# Define a data file to invert
filepath = '/Users/cberube/Repositories/bisip/data files/SIP-K389175_avg.dat'
# Fit the model to this data file
model.fit(filepath)
```
```
Out:
100%|██████████| 1000/1000 [00:01<00:00, 558.64it/s]
```

```python
# Plot the parameter traces
fig = model.plot_traces()
```
<p align="center">
    <img src="https://raw.githubusercontent.com/clberube/bisip2/master/figures/traces.png" width="100%">
</p>

<img src="https://raw.githubusercontent.com/clberube/bisip2/master/figures/fitted.png" width="25%" align="right">

```python
# Extract the parameter values for all walkers
# after a <discard> period.
# Thin the chain by selecting every <thin> steps
# Flatten the walkers into a single chain
chain = model.get_chain(discard=300,
                        thin=30,
                        flat=True)

# Plot the model against the data for
# the remaining parameter values in the chain
fig = model.plot_fit(chain)
```
