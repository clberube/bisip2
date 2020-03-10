#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 10-03-2020


import emcee
import numpy as np

from .cython_funcs import Decomp_cyth, ColeCole_cyth
from . import utils
from . import plotlib


class Inversion(plotlib.plotlib, utils.utils):
    """An abstract class to perform inversion of SIP data.

    This class is the base constructor for the PolynomialDecomposition and
    ColeCole classes.

    Args:
        nwalkers (:obj:`int`): Number of walkers to use to explore the
            parameter space. Defaults to 32.
        nsteps (:obj:`int`): Number of steps to perform in the MCMC
            simulation. Defaults to 5000.
        pool (:obj:`pool`, optional): A pool object from the multiprocessing
            library. See
            https://emcee.readthedocs.io/en/stable/tutorials/parallel/.
            Defaults to None.
        moves (:obj:`moves`, optional): A `emcee` Moves class (see
            https://emcee.readthedocs.io/en/stable/user/moves/). If None,
            the emcee algorithm `StretchMove` is used. Defaults to None.

    """

    def __init__(self, nwalkers=32, nsteps=5000, pool=None, moves=None):
        self.nsteps = nsteps
        self.nwalkers = nwalkers
        self.pool = pool
        self.moves = moves
        self._params = {}
        self.__fitted = False

    def _log_likelihood(self, theta, f, x, y, yerr):
        """Returns the conditional log-likelihood of the observations. """
        sigma2 = yerr**2
        return -0.5*np.sum((y - f(theta, x))**2 / sigma2 + 2*np.log(sigma2))

    def _log_prior(self, theta, bounds):
        """Returns the prior log-probability of the model parameters. """
        if not ((bounds[0] < theta).all() and (theta < bounds[1]).all()):
            return -np.inf
        else:
            return 0.0

    def _log_probability(self, theta, model, bounds, x, y, yerr):
        """Returns the Bayes numerator log-probability. """
        lp = self._log_prior(theta, bounds)
        if not np.isfinite(lp):
            return -np.inf
        return lp + self._log_likelihood(theta, model, x, y, yerr)

    def _check_if_fitted(self):
        """Checks if the model has been fitted. """
        if not self.fitted:
            raise AssertionError('Model is not fitted! Fit the model to a '
                                 'dataset before attempting to plot results.')

    def get_chain(self, **kwargs):
        """Gets the MCMC chains from a fitted model.

        Keyword Args:
            discard (:obj:`int`): Number of steps to discard (burn-in period).
            thin (:obj:`int`): Thinning factor.
            flat (:obj:`bool`): Whether or not to flatten the walkers. If flat
                is False, the output chain will have shape (nsteps, nwalkers,
                ndim). If flat is True, the output chain will have shape
                (nsteps*nwalkers, ndim).

        Returns:
            :obj:`ndarray`: The MCMC chain(s).

        """
        return self.sampler.get_chain(**kwargs)

    def fit(self, **kwargs):
        """Samples the posterior distribution to fit the model to the data.

        Keyword Args:
            **kwargs: Additional keyword arguments passed to the
                EnsembleSampler class (see
                https://emcee.readthedocs.io/en/stable/user/sampler/).

        """
        self.ndim = self._bounds.shape[1]
        self.p0 = np.random.uniform(*self._bounds, (self.nwalkers, self.ndim))

        model_args = (self.forward, self._bounds, self.data['w'],
                      self.data['zn'], self.data['zn_err'])

        self.sampler = emcee.EnsembleSampler(self.nwalkers,
                                             self.ndim,
                                             self._log_probability,
                                             args=model_args,
                                             **kwargs,
                                             )
        self.sampler.run_mcmc(self.p0, self.nsteps, progress=True)
        self.__fitted = True

    @property
    def params(self):
        """:obj:`dict`: Parameter names and their bounds."""
        return self._params

    @params.setter
    def params(self, var):
        self._params = var

    @property
    def fitted(self):
        return self.__fitted

    @property
    def param_names(self):
        """:obj:`list` of :obj:`str`: Ordered names of the parameters."""
        return list(self.params.keys())

    @property
    def param_bounds(self):
        """:obj:`list` of :obj:`float`: Ordered bounds of the parameters."""
        return list(self.params.values())


class PolynomialDecomposition(Inversion):
    """A polynomial decomposition inversion scheme for SIP data.

    Args:
        poly_deg (:obj:`int`): The polynomial degree to use for the
            decomposition. Defaults to 5.
        c_exp (:obj:`float`): The c-exponent to use for the decomposition
            scheme. 0.5 -> Warburg, 1.0 -> Debye. Defaults to 1.0.

    """

    def __init__(self, filepath, poly_deg=5, c_exp=1.0, headers=1,
                 ph_units='mrad', **kwargs):
        super().__init__(**kwargs)
        self.c_exp = c_exp
        self.poly_deg = poly_deg

        # Load data
        self.data = self.load_data(filepath, headers, ph_units)

        # Define a range of relaxation time values for the RTD
        min_tau = np.floor(min(np.log10(1./self.data['w'])) - 1)
        max_tau = np.floor(max(np.log10(1./self.data['w'])) + 1)
        n_tau = 2*self.data['N']
        self.log_tau = np.linspace(min_tau, max_tau, n_tau)

        # Precompute the log_tau_i**i values for the polynomial approximation
        deg_range = list(range(self.poly_deg+1))
        self.log_taus = np.array([self.log_tau**i for i in deg_range])
        self.taus = 10**self.log_tau  # Accelerates sampling

        # Add polynomial decomposition parameters to dict
        self.params.update({'r0': [0.9, 1.1]})
        self.params.update({f'a{x}': [-1, 1] for x in deg_range})

        self._bounds = np.array(self.param_bounds).T

    def forward(self, theta, w):
        """Returns a Polynomial Decomposition impedance.

        Args:
            theta (:obj:`ndarray`): Ordered array of R0, a_{poly_deg},
                a_{poly_deg-1}, ..., a_{0}. See
                https://doi.org/10.1016/j.cageo.2017.05.001.
            w (:obj:`ndarray`): Array of angular frequencies to compute the
                impedance for (w = 2*pi*f).

        """
        return Decomp_cyth(w, self.taus, self.log_taus, self.c_exp,
                           R0=theta[0], a=theta[1:])


class ColeCole(Inversion):
    """A generalized ColeCole inversion scheme for SIP data.

    Args:
        n_modes (:obj:`int`): The number of ColeCole modes to use for the
            inversion. Defaults to 1.

    """

    def __init__(self, filepath, n_modes=1, headers=1, ph_units='mrad',
                 **kwargs):
        super().__init__(**kwargs)
        self.n_modes = n_modes

        # Load data
        self.data = self.load_data(filepath, headers, ph_units)

        # Add multi-mode ColeCole parameters to dict
        range_modes = list(range(self.n_modes))
        self.params.update({'r0': [0.9, 1.1]})
        self.params.update({f'm{i+1}': [0.0, 1.0] for i in range_modes})
        self.params.update({f'log_tau{i+1}': [-20, 10] for i in range_modes})
        self.params.update({f'c{i+1}': [0.0, 1.0] for i in range_modes})

        self._bounds = np.array(self.param_bounds).T

    def forward(self, theta, w):
        """Returns a ColeCole impedance.

        Args:
            theta (:obj:`ndarray`): Ordered array of R0, m_{1}, ...,
                m_{n_modes}, log_tau_{1}, ..., log_tau_{n_modes}, c_{1}, ...,
                c_{n_modes}. See https://doi.org/10.1016/j.cageo.2017.05.001.
            w (:obj:`ndarray`): Array of angular frequencies to compute the
                impedance for (w = 2*pi*f).

        """
        return ColeCole_cyth(w,
                             R0=theta[0],
                             m=theta[1:1+self.n_modes],
                             lt=theta[1+self.n_modes:1+2*self.n_modes],
                             c=theta[1+2*self.n_modes:])
