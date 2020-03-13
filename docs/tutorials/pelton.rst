.. _Pelton:

The Pelton Cole-Cole model
==========================

In this tutorial we will show that the parameter space of the generalized
Cole-Cole model can be quite complex for some data sets.

`Pelton (1978) <https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JB077i026p04945>`_
noted that the complex resistivity spectra of rocks :math:`\boldsymbol{\rho^*}`
could be interpreted using Cole-Cole relaxation models:

.. math::
  \boldsymbol{\rho^*} = \rho_0 \left[ 1-m\left(1-\frac{1}{1+(i\boldsymbol{\omega}\tau)^c} \right) \right],

where :math:`\boldsymbol{\omega}` is the vector of angular measurement frequencies
(:math:`\omega=2\pi f`) and :math:`i` is the imaginary unit.

BISIP implements the generalized form of the Pelton Cole-Cole model given by
`Chen et al., (2008) <https://doi.org/10.1190/1.2976115>`_:

.. math::
  \boldsymbol{\rho^*} = \rho_0 \left[ 1 - \sum_{k=1}^{K} m_k\left(1-\frac{1}{1+(i\boldsymbol{\omega}\tau_k)^c_k} \right) \right],

where the subscript :math:`k` refers to one of :math:`K` superimposed Cole-Cole
relaxation modes. Here, :math:`\rho^*` depends on :math:`1 + 3K` parameters:

  - :math:`\rho_0 \in [0, \infty)`, the direct current resistivity :math:`\rho_0 = \rho (\omega\to 0)`.
  - :math:`m_k \in [0, 1]`, each mode's chargeability :math:`m=(\rho_0 - \rho_\infty)/\rho_0`.
  - :math:`\tau_k \in [0, \infty)`, each mode's relaxation time, related to
    average polarizable particle size.
  - :math:`c_k \in [0, 1]`, the slope of the measured phase shift for each mode.
