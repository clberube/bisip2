#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 05-03-2020


import emcee
import numpy as np
from .cython_funcs import Decomp_cyth
from . import utils
from . import plotlib


def log_likelihood(theta, model, x, y, yerr):
    # sigma2 = yerr ** 2 + model(theta, x) ** 2 * np.exp(2 * theta[1])
    sigma2 = yerr**2
    return -0.5 * np.sum((y - model(theta, x)) ** 2 / sigma2 + np.log(sigma2))


def log_prior(theta, bounds):
    if (bounds[0] < theta).all() and (theta < bounds[1]).all():
        return 0.0
    return -np.inf


def log_probability(theta, model, bounds, x, y, yerr):
    lp = log_prior(theta, bounds)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta, model, x, y, yerr)


class Inversion(object):

    plot_traces = plotlib.plot_traces
    plot_histograms = plotlib.plot_histograms
    plot_fit = plotlib.plot_fit

    def __init__(self, pool=None, moves=None):
        self.pool = pool
        self.moves = moves

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

    def get_chain(self, **kwargs):
        return self.sampler.get_chain(**kwargs)


class PolynomialDecomposition(Inversion):

    def __init__(self, nwalkers=32, poly_deg=5, c_exp=1.0, nsteps=5000):
        super(PolynomialDecomposition, self).__init__()
        self.c_exp = c_exp
        self.nsteps = nsteps
        self.nwalkers = nwalkers
        self.poly_deg = poly_deg

    def forward(self, theta, w):
        rho, *a = theta
        a = np.array(a)
        return Decomp_cyth(w, self.taus, self.log_taus, self.c_exp, rho, a)

    def fit(self, filepath, **data_kwargs):
        self.data = utils.load_data(filepath, **data_kwargs)

        min_tau = np.floor(min(np.log10(1./self.data['w'])) - 1)
        max_tau = np.floor(max(np.log10(1./self.data['w'])) + 1)
        n_tau = 2*self.data['N']
        self.log_tau = np.linspace(min_tau, max_tau, n_tau)

        deg_range = list(range(self.poly_deg+1))
        rev_deg_range = list(reversed(deg_range))
        self.log_taus = np.array([self.log_tau**i for i in rev_deg_range])
        self.taus = 10**self.log_tau  # Accelerates sampling

        params = {'r0': [0.9, 1.1]}
        params.update({f'a{x}': [-1, 1] for x in rev_deg_range})

        self.bounds = np.array([params[x] for x in params.keys()]).T
        self.params = params

        # self.bounds = np.array([[0.9, 0] + [-1 for i in deg_range],
        #                         [1.1, 1] + [1 for i in deg_range],
        #                         ])

        self._start_sampling(pool=self.pool, moves=self.moves)
