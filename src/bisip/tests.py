#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   12-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 12-03-2020


import warnings

import matplotlib.pyplot as plt

from bisip import PolynomialDecomposition, ColeCole


def run_test():

    fp = f'./data/SIP-K389175.dat'

    print('Testing ColeCole fits with nsteps=1000')
    model = ColeCole(fp, nwalkers=32, n_modes=2, nsteps=1000)
    model.fit()

    # Get the mean parameter values and their std
    # discarding the first 1000 steps (burn-in)
    values = model.get_param_mean(discard=800)
    uncertainties = model.get_param_std(discard=800)

    for n, v, u in zip(model.param_names, values, uncertainties):
        print(f'{n}: {v:.5f} +/- {u:.5f}')

    print('Testing Debye Decomposition with nsteps=2000')
    model = PolynomialDecomposition(fp, nwalkers=32, poly_deg=4, nsteps=2000)
    # Update parameter boundaries inplace
    # model.params.update(a0=[-2, 2])
    model.fit()

    chain = model.get_chain(discard=1000, thin=1, flat=True)

    # Get the mean parameter values and their std
    # discarding the first 1000 steps (burn-in)
    values = model.get_param_mean(chain)
    uncertainties = model.get_param_std(chain)

    for n, v, u in zip(model.param_names, values, uncertainties):
        print(f'{n}: {v:.5f} +/- {u:.5f}')

    print('Testing plotlib')
    fig = model.plot_traces()
    # fig.savefig('./docs/tutorials/figures/ex1_traces.png', dpi=144, bbox_inches='tight')
    plt.show(block=False)

    fig = model.plot_histograms(chain)
    # fig.savefig('./figures/histograms.png', dpi=144, bbox_inches='tight')
    plt.close()

    fig = model.plot_fit(chain)
    # fig.savefig('./figures/fitted.png', dpi=144, bbox_inches='tight')
    plt.show(block=False)

    try:
        fig = model.plot_corner(chain)
        plt.close()
        # fig.savefig('./figures/corner.png', dpi=144, bbox_inches='tight')
    except ImportError:
        warnings.warn('The `corner` package was not found. Install it with '
                      '`conda install corner`')

    print('All tests passed. Press ctrl+C or close figure windows to exit.')
    plt.show()
