#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 09-03-2020


import numpy as np
import matplotlib.pyplot as plt
from corner import corner

from src.bisip import PolynomialDecomposition, ColeCole


if __name__ == '__main__':
    fp = f'./data/SIP-K389175.dat'

    print('Testing ColeCole fits')
    model = ColeCole(nwalkers=32, n_modes=2, nsteps=1000)
    model.fit(fp)

    print('Testing Debye Decomposition')
    model = PolynomialDecomposition(nwalkers=32, poly_deg=4, c_exp=1.0, nsteps=1000)
    model.fit(fp)

    chain = model.get_chain(discard=200, thin=1, flat=True)

    # Get the parameter values for the 2.5th, 50th and 97.5th percentiles
    # discarding the first 200 steps (burn-in)
    values = model.get_param_mean(discard=200)
    uncertainties = model.get_param_std(discard=200)

    for n, v, u in zip(model.param_names, values, uncertainties):
        print(f'{n}: {v:.5f} +/- {u:.5f}')

    print('Testing plotlib')
    fig = model.plot_traces()
    # fig.savefig('./figures/traces.png', dpi=144, bbox_inches='tight')

    fig = model.plot_histograms(chain)
    # fig.savefig('./figures/histograms.png', dpi=144, bbox_inches='tight')

    fig = model.plot_fit(chain)
    # fig.savefig('./figures/fitted.png', dpi=144, bbox_inches='tight')

    fig = model.plot_corner(chain)
    # fig.savefig('./figures/corner_plot.png', dpi=144, bbox_inches='tight')

    print('All tests passed')
