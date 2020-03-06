#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   charles
# @Last modified time: 2020-03-06T12:36:16-05:00


from os.path import expanduser
import numpy as np
import matplotlib.pyplot as plt

from src.bisip.models import PolynomialDecomposition


HOME = expanduser("~")

model = PolynomialDecomposition(nwalkers=32, poly_deg=4, c_exp=1.0, nsteps=1000)

fp = f'{HOME}/Repositories/bisip/data files/SIP-K389175_avg.dat'
model.fit(fp)

fig = model.plot_traces()
fig.savefig('./figures/traces.png', dpi=144, bbox_inches='tight')

chain = model.get_chain(discard=300, thin=30, flat=True)

# fig = model.plot_histograms(chain=chain)
# fig.savefig('./figures/histograms.png', dpi=144, bbox_inches='tight')
fig = model.plot_fit(chain)
fig.savefig('./figures/fitted.png', dpi=144, bbox_inches='tight')
# model.get_model_percentile(chain)

# model.get_param_percentile(chain, [2.5, 50, 97.5])
