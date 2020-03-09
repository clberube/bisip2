#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 09-03-2020


import emcee
import numpy as np

from .cython_funcs import Decomp_cyth, ColeCole_cyth
from . import utils
from . import plotlib


def log_likelihood(theta, model, x, y, yerr):
    """
    """
    sigma2 = yerr**2
    return -0.5 * np.sum((y - model(theta, x))**2 / sigma2 + 2*np.log(sigma2))


def log_prior(theta, bounds):
    if not ((bounds[0] < theta).all() and (theta < bounds[1]).all()):
        return -np.inf
    else:
        return 0.0


def log_probability(theta, model, bounds, x, y, yerr):
    lp = log_prior(theta, bounds)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta, model, x, y, yerr)


class Inversion(plotlib.plotlib, utils.utils):

    def __init__(self, nwalkers=32, nsteps=5000, pool=None, moves=None):
        """An abstract class to perform inversion of SIP data.

        This class is the base constructor for the PolynomialDecomposition and
        ColeCole classes.

        Args:
            nwalkers (:obj:`str`): Number of walkers to use to explore the
                parameter space. Defaults to 32.
            nsteps (:obj:`int`): Number of steps to perform in the MCMC
                simulation. Defaults to 5000.

        """
        self.nsteps = nsteps
        self.nwalkers = nwalkers
        self.pool = pool
        self.moves = moves
        self.params = {}
        self.__fitted = False

    def _start_sampling(self, **kwargs):
        self.ndim = self.bounds.shape[1]
        self.p0 = np.random.uniform(*self.bounds, (self.nwalkers, self.ndim))

        model_args = (self.forward, self.bounds, self.data['w'],
                      self.data['zn'], self.data['zn_err'])

        self.sampler = emcee.EnsembleSampler(self.nwalkers,
                                             self.ndim,
                                             log_probability,
                                             args=model_args,
                                             **kwargs,
                                             )
        self.sampler.run_mcmc(self.p0, self.nsteps, progress=True)
        self.__fitted = True

    def get_chain(self, **kwargs):
        """Filters a chain by discarding

        Keyword Arguments:
            discard (:obj:`int`): Number of steps to discard (burn-in period).
            thin (:obj:`int`): Thinning factor.
            flat (:obj:`bool`): Whether or not to flatten the walkers.
        """
        return self.sampler.get_chain(**kwargs)

    def get_model_percentile(self, p, chain=None, **kwargs):
        """Gets percentiles of the model values for a MCMC chain.

        Args:
            p (:obj:`float` or :obj:`list` of :obj:`float`): percentiles values
                to compute.

        Keyword Arguments:
            See kwargs of the `get_chain()` method.
        """
        chain = self.parse_chain(chain, **kwargs)
        results = np.empty((chain.shape[0], 2, self.data['N']))
        for i in range(chain.shape[0]):
            results[i] = self.forward(chain[i], self.data['w'])
        return np.percentile(results, p, axis=0)

    def get_param_percentile(self, p, chain=None, **kwargs):
        """Gets percentiles of the parameter values for a MCMC chain.

        Args:
            p (:obj:`float` or :obj:`list` of :obj:`float`): percentiles values
                to compute.

        Keyword Arguments:
            See kwargs of the `get_chain()` method.
        """
        chain = self.parse_chain(chain, **kwargs)
        return np.percentile(chain, p, axis=0)

    def get_param_mean(self, chain=None, **kwargs):
        """Gets the mean of the model parameters for a MCMC chain.

        Keyword Arguments:
            See kwargs of the `get_chain()` method.
        """
        chain = self.parse_chain(chain, **kwargs)
        return np.mean(chain, axis=0)

    def get_param_std(self, chain=None, **kwargs):
        """Gets the standard deviation of the model parameters for a MCMC
            chain.

        Keyword Arguments:
            See kwargs of the `get_chain()` method.
        """
        chain = self.parse_chain(chain, **kwargs)
        return np.std(chain, axis=0)

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
        return self.bounds


class PolynomialDecomposition(Inversion):

    def __init__(self, poly_deg=5, c_exp=1.0, **kwargs):
        """A polynomial decomposition inversion scheme for SIP data.

        Args:
            poly_deg (:obj:`int`): The polynomial degree to use for the
                decomposition. Defaults to 5.
            c_exp (:obj:`float`): The c-exponent to use for the decomposition
                scheme. 0.5 -> Warburg, 1.0 -> Debye. Defaults to 1.0.

        """
        super().__init__(**kwargs)
        self.c_exp = c_exp
        self.poly_deg = poly_deg

    def forward(self, theta, w):
        return Decomp_cyth(w, self.taus, self.log_taus, self.c_exp,
                           R0=theta[0], a=theta[1:])

    def fit(self, filepath, **data_kwargs):
        self.data = self.load_data(filepath, **data_kwargs)

        min_tau = np.floor(min(np.log10(1./self.data['w'])) - 1)
        max_tau = np.floor(max(np.log10(1./self.data['w'])) + 1)
        n_tau = 2*self.data['N']
        self.log_tau = np.linspace(min_tau, max_tau, n_tau)

        deg_range = list(range(self.poly_deg+1))
        rev_deg_range = list(reversed(deg_range))
        self.log_taus = np.array([self.log_tau**i for i in rev_deg_range])
        self.taus = 10**self.log_tau  # Accelerates sampling

        # Add polynomial decomposition parameters to dict
        self.params.update({'r0': [0.9, 1.1]})
        self.params.update({f'a{x}': [-1, 1] for x in rev_deg_range})

        self.bounds = np.array([self.params[x] for x in self.params.keys()]).T

        self._start_sampling(pool=self.pool, moves=self.moves)


class ColeCole(Inversion):

    def __init__(self, n_modes=1, **kwargs):
        """A generalized ColeCole inversion scheme for SIP data.

        Args:
            n_modes (:obj:`int`): The number of ColeCole modes to use for the
                inversion. Defaults to 1.

        """
        super().__init__(**kwargs)
        self.n_modes = n_modes

    def forward(self, theta, w):
        return ColeCole_cyth(w,
                             R0=theta[0],
                             m=theta[1:1+self.n_modes],
                             lt=theta[1+self.n_modes:1+2*self.n_modes],
                             c=theta[1+2*self.n_modes:])

    def fit(self, filepath, **data_kwargs):
        self.data = self.load_data(filepath, **data_kwargs)

        # Add polynomial decomposition parameters to dict
        range_modes = list(range(self.n_modes))
        self.params.update({'r0': [0.9, 1.1]})
        self.params.update({f'm{i+1}': [0.0, 1.0] for i in range_modes})
        self.params.update({f'log_tau{i+1}': [-20, 10] for i in range_modes})
        self.params.update({f'c{i+1}': [0.0, 1.0] for i in range_modes})

        self.bounds = np.array([self.params[x] for x in self.params.keys()]).T

        self._start_sampling(pool=self.pool, moves=self.moves)
