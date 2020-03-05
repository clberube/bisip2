# BISIP
## This is the development repository for BISIP2, the successor of BISIP: https://github.com/clberube/BISIP
### BISIP is being re-written from scratch with better code practice, documentation, and most importantly with a more powerful Ensemble MCMC sampler.




### Installation

### Quickstart
```python
from bisip import PolynomialDecomposition

# Define a Polynomial Decomposition model with
# a 4th order approximation and c-exponent equal to 1 (Debye)
# The simulation will run for 5000 steps with 32 walkers
# exploring the Debye Decomposition parameter space
model = PolynomialDecomposition(nwalkers=32,  # number of walkers
                                nsteps=5000,  # number of MCMC steps
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
100%|██████████| 5000/5000 [00:09<00:00, 512.08it/s]
```

```python
# Plot the parameter parameter traces
fig = model.plot_traces()
```
```
Out:

```

```python
# Extract the parameter values for all walkers after a <discard> period
# Thin is by taking every 10 iterations (depending on autocorrelation)
# Flatten the walkers into a single chain
chain = model.get_chain(discard=1000, thin=10, flat=True)

# Plot the model against the data for these parameter values
fig = model.plot_fit(chain)
```
```
Out:

```
