BISIP
=====

**BISIP** is an MIT licensed Python implementation of Goodman & Weare's
Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler to perform
Bayesian Inversion of Spectral Induced Polarization data. See our original
`paper <https://ui.adsabs.harvard.edu/abs/2017CG....105...51B/abstract>`_ in
Computers & Geosciences for more details. BISIP relies on
`emcee <https://emcee.readthedocs.io/en/stable/>`_ to explore the SIP models'
parameter spaces with multiple walkers. You can find a link to the paper
explaining the emcee algorithm and implementation in detail
`here <https://arxiv.org/abs/1202.3665>`_.

BISIP is being actively developed on `GitHub
<https://github.com/clberube/bisip2>`_.


Basic Usage
-----------

If you wanted to draw samples from a 5 dimensional Gaussian, you would do
something like:

.. code-block:: python

    import numpy as np
    import emcee

    def log_prob(x, ivar):
        return -0.5 * np.sum(ivar * x ** 2)

    ndim, nwalkers = 5, 100
    ivar = 1. / np.random.rand(ndim)
    p0 = np.random.randn(nwalkers, ndim)

    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob, args=[ivar])
    sampler.run_mcmc(p0, 10000)

A more complete example is available in the :ref:`quickstart` tutorial.

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
