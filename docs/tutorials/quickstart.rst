In this first tutorial we load a data file, perform Debye decomposition on it,
visualize the fit quality and posterior distribution and save results to a csv
file.

====

Basic Usage
-----------

To perform Debye Decomposition of a SIP data file, you would use the following:
First, define a Polynomial Decomposition model with a 4th order approximation
and c-exponent equal to 1 (Debye). Set the simulation to run for 1000 steps
with 32 MCMC walkers exploring the Debye Decomposition parameter space.

.. code-block:: python
  :linenos:

  from bisip import PolynomialDecomposition

  # Use one of the example data files provided with BISIP
  filepath = '/path/to/bisip/data/SIP-K389175.dat'

  model = PolynomialDecomposition(filepath=filepath,
                                  nwalkers=32,  # number of MCMC walkers
                                  nsteps=1000,  # number of MCMC steps
                                  poly_deg=4,  # 4th order polynomial
                                  c_exp=1.0,  # debye decomposition
                                  )

  # Fit the model to this data file
  model.fit()

  #   Out:  100%|██████████| 1000/1000 [00:01<00:00, 563.92it/s]

  # Print out the optimal parameters and their uncertainties
  # discarding the first 200 steps (burn-in)
  values = model.get_param_mean(discard=200)
  uncertainties = model.get_param_std(discard=200)

  for n, v, u in zip(model.param_names, values, uncertainties):
      print(f'{n}: {v:.5f} +/- {u:.5f}')

  #   Out:  r0: 0.99822 +/- 0.00787
  #         a4: 0.00023 +/- 0.00005
  #         a3: 0.00082 +/- 0.00032
  #         a2: -0.00124 +/- 0.00048
  #         a1: -0.00405 +/- 0.00060
  #         a0: 0.00677 +/- 0.00058
