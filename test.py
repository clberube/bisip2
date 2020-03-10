#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 10-03-2020


import warnings

import numpy as np
import matplotlib.pyplot as plt
from corner import corner

from src.bisip import PolynomialDecomposition, ColeCole

# if __name__ == '__main__':
fp = f'./data/SIP-K389175.dat'

print('Testing ColeCole fits with nsteps=1000')
model = ColeCole(nwalkers=32, n_modes=2, nsteps=1000)
model.fit(fp)

# Get the mean parameter values and their std
# discarding the first 1000 steps (burn-in)
values = model.get_param_mean(discard=800)
uncertainties = model.get_param_std(discard=800)

for n, v, u in zip(model.param_names, values, uncertainties):
    print(f'{n}: {v:.5f} +/- {u:.5f}')

print('Testing Debye Decomposition with nsteps=2000')
model = PolynomialDecomposition(nwalkers=32, poly_deg=4, nsteps=2000)
model.fit(fp)

chain = model.get_chain(discard=1000, thin=1, flat=True)

# Get the mean parameter values and their std
# discarding the first 1000 steps (burn-in)
values = model.get_param_mean(chain)
uncertainties = model.get_param_std(chain)

for n, v, u in zip(model.param_names, values, uncertainties):
    print(f'{n}: {v:.5f} +/- {u:.5f}')

print('Testing plotlib')
fig = model.plot_traces()
# fig.savefig('./figures/traces.png', dpi=144, bbox_inches='tight')
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
    # fig.savefig('./figures/corner_plot.png', dpi=144, bbox_inches='tight')
except ImportError:
    warnings.warn('The `corner` package was not found. Install it with '
                  '`conda install corner`')

print('All tests passed. Press ctrl+C or close figure windows to exit.')
plt.show()
