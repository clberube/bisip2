BISIP
=====

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

To perform Debye Decomposition of a SIP data file, you would use the following:

.. code-block:: python

  from bisip import PolynomialDecomposition
  # Define a Polynomial Decomposition model with
  # a 4th order approximation and c-exponent equal to 1 (Debye)
  # The simulation will run for 1000 steps with 32 walkers
  # exploring the Debye Decomposition parameter space
  model = PolynomialDecomposition(nwalkers=32,  # number of walkers
                                  nsteps=1000,  # number of MCMC steps
                                  poly_deg=4,  # 4th order polynomial
                                  c_exp=1.0,  # debye decomposition
                                  )

  # Define a data file to invert
  filepath = '/Users/cberube/Repositories/bisip/data files/SIP-K389175_avg.dat'
  # Fit the model to this data file
  model.fit(filepath)
    100%|██████████| 1000/1000 [00:01<00:00, 558.64it/s]


A more detailed guide is available in the :ref:`quickstart` tutorial.

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user/install
   user/models
   user/plot


.. toctree::
   :maxdepth: 1
   :caption: Tutorials

   tutorials/quickstart
