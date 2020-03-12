BISIP
=====
**DOCUMENTATION IS UNDER CONSTRUCTION**

**BISIP** is an MIT licensed Python package to perform Bayesian Inversion of
Spectral Induced Polarization data with Markov-chain Monte Carlo simulation.
See our original
`paper <https://ui.adsabs.harvard.edu/abs/2017CG....105...51B/abstract>`_ in
Computers & Geosciences for more details. BISIP uses `Goodman & Weare's Affine
Invariant Ensemble sampler
<https://projecteuclid.org/euclid.camcos/1513731992>`_ as
implemented in `emcee <https://emcee.readthedocs.io/en/stable/>`_ to explore
the SIP models' parameter spaces with multiple walkers. You can read the paper
by Foreman-Mackey et al. explaining the emcee algorithm in detail
`here <https://arxiv.org/abs/1202.3665>`_.

BISIP is being developed on `GitHub
<https://github.com/clberube/bisip2>`_.


Basic Usage
-----------

To perform Inversion of a SIP data file, you would use the following approach:

- Import the base :code:`Polynomial Decomposition` model.
- Pass :code:`filepath` to instantiate the model with a specific data file.
- Pass the :code:`poly_deg=4` argument to specify a 4th order approximation.
- Pass the :code:`c_exp=1.0` argument to specifiy a Debye decomposition model.
- Set the simulation to run for 1000 steps by passing :code:`nsteps=1000`.
- Set the simulation to explore the Debye decomposition parameter space with
    :code:`nwalkers=32`.

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


A more detailed example is available in the :ref:`Quickstart` tutorial.

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user/install
   user/models
   user/data_format


.. toctree::
   :maxdepth: 1
   :caption: Tutorials

   tutorials/quickstart
   tutorials/decomposition
