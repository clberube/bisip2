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

To perform Debye Decomposition of a SIP data file, you would use the following:
First, define a Polynomial Decomposition model with a 4th order approximation
and c-exponent equal to 1 (Debye). Set the simulation to run for 1000 steps
with 32 MCMC walkers exploring the Debye Decomposition parameter space.

.. code-block:: python

  from bisip import PolynomialDecomposition

  model = PolynomialDecomposition(nwalkers=32,  # number of MCMC walkers
                                  nsteps=1000,  # number of MCMC steps
                                  poly_deg=4,  # 4th order polynomial
                                  c_exp=1.0,  # debye decomposition
                                  )

  # Use one of the example data files provided with BISIP
  filepath = '/path/to/bisip/data/SIP-K389175.dat'

  # Fit the model to this data file
  model.fit(filepath)
  # Out: 100%|██████████| 1000/1000 [00:01<00:00, 558.64it/s]

You can then plot the parameter space with:

.. code-block:: python

  model.plot_corner(discard=200)

.. image:: https://raw.githubusercontent.com/clberube/bisip2/master/figures/corner_plot.png


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
