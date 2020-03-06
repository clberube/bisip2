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

If you wanted to draw samples from a 5 dimensional Gaussian, you would do
something like:

.. code-block:: python

    import numpy as np


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
