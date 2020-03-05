#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 05-03-2020


import numpy as np
from src.bisip.models import PolynomialDecomposition


model = PolynomialDecomposition(nwalkers=32, poly_deg=4, c_exp=1.0, nsteps=5000)

fp = '/Users/cberube/Repositories/bisip/data files/SIP-K389175_avg.dat'
model.fit(fp)

fig = model.plot_traces(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])

chain = model.get_chain(discard=1000, thin=10, flat=True)
chain.shape

fig = model.plot_histograms(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], chain=chain)


fig = model.plot_fit(chain)
