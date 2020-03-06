#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   charles
# @Last modified time: 2020-03-06T17:11:03-05:00


from os.path import expanduser
import numpy as np
import matplotlib.pyplot as plt
from corner import corner

from src.bisip.models import PolynomialDecomposition, ColeCole


HOME = expanduser("~")

model = PolynomialDecomposition(nwalkers=32, poly_deg=4, c_exp=1.0, nsteps=1000)
# model = ColeCole(nwalkers=32, n_modes=2, nsteps=1000)

fp = f'{HOME}/Repositories/bisip/data files/SIP-K389175_avg.dat'
model.fit(fp)

fig = model.plot_traces()
# fig.savefig('./figures/traces.png', dpi=144, bbox_inches='tight')

chain = model.get_chain(discard=200, thin=1, flat=True)

# Get the parameter values for the 2.5th, 50th and 97.5th percentiles
# discarding the first 200 steps (burn-in)
values = model.get_param_mean(discard=200)
uncertainties = model.get_param_std(discard=200)

for n, v, u in zip(model.param_names, values, uncertainties):
    print(f'{n}: {v:.5f} +/- {u:.5f}')


fig = model.plot_histograms(chain=chain)
# fig.savefig('./figures/histograms.png', dpi=144, bbox_inches='tight')

fig = model.plot_fit(chain)
# fig.savefig('./figures/fitted.png', dpi=144, bbox_inches='tight')

fig = model.plot_corner(chain)
fig.savefig('./figures/corner_plot.png', dpi=144, bbox_inches='tight')
