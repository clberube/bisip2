.. _Dias:

The Dias (2000) model
=====================

In this tutorial we will explore the parameter space of the SIP model proposed by
`Dias (1972) <https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JB077i026p04945>`_.
This semi-empirical model describes the petrophysical properties of rocks through
measurements of their electrical polarization in a frequency range typically from
1 mHz to 100 kHz. We refer to `Dias (2000) <https://library.seg.org/doi/10.1190/1.1444738>`_
for the implementation of the complex resistivity formula in BISIP. This model
predicts that the complex resistivity :math:`\rho^*` of a polarizable rock sample
can be described by

.. math::
  \rho^* = \rho_0 \left[ 1-m\left(1-\frac{1}{1+i\omega\tau'(1+\frac{1}{\mu})} \right) \right],

where :math:`\mu = i\omega\tau + \left(i\omega\tau''\right)^{1/2}`,
:math:`\tau' = (\tau/\delta)(1 - \delta)/(1 - m)`
and :math:`\tau'' = \tau^2 \eta^2`.

Here, :math:`\rho^*` depends on 5 parameters:

- :math:`\rho_0 \in [0, \infty(`, the direct current resistivity :math:`\rho_0 = \rho (\omega\to 0` ).
- :math:`m \in [0, 1)`, the chargeability :math:`m=(\rho_0 - \rho_\infty)/\rho_0`.
- :math:`\tau \in [0, \infty(`, the relaxation time, related to
  average polarizable particle size.
- :math:`\eta \in [0, 150]`, characteristic of the
  electrochemical environment producing polarization.
- :math:`\delta \in [0, 1)`, the pore length fraction of the electrical double
  layer zone in the material.
