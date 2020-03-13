# @Author: charles
# @Date:   2020-03-13T10:32:45-04:00
# @Last modified by:   charles
# @Last modified time: 2020-03-13T11:28:25-04:00


import os
import pathlib

import numpy as np
import matplotlib.pyplot as plt

import bisip
from bisip import Dias2000


cfp = pathlib.Path(__file__).parent.parent.absolute()

if __name__ == '__main__':
    fp = f'data/SIP-K389172.dat'
    fp = os.path.join(os.path.dirname(bisip.__file__), fp)

    nwalkers = 32
    nsteps = 2000
    model = Dias2000(filepath=fp, nwalkers=nwalkers, nsteps=nsteps)
    model.fit()

    fig = model.plot_traces()
    dst_p = os.path.join(cfp, 'figures/')
    # fig.savefig(dst_p+'dias_wide_traces.png', dpi=144, bbox_inches='tight')
    plt.close()

    model.params.update(eta=[0, 25], log_tau=[-15, -5])
    model.p0 = None

    model.fit()
    fig = model.plot_traces()
    # fig.savefig(dst_p+'dias_bounds_updated.png', dpi=144, bbox_inches='tight')
    plt.close()

    fig = model.plot_fit(discard=500)
    # fig.savefig(dst_p+'dias_fit.png', dpi=144, bbox_inches='tight')
    plt.close()

    # start = np.vstack([[1.0, 0.25, -10, 5, 0.5] for _ in range(32)])
    # model.p0 = start + 1e-1*start*(np.random.rand(*start.shape) - 1)
    # # Update parameter boundaries inplace
    # # model.params.update(a0=[-2, 2])
    # model.fit()
    #
    # chain = model.get_chain(discard=1000, thin=1, flat=True)
    # # Get the mean parameter values and their std
    # # discarding the first 1000 steps (burn-in)
    # values = model.get_param_mean(chain)
    # uncertainties = model.get_param_std(chain)
    #
    # for n, v, u in zip(model.param_names, values, uncertainties):
    #     print(f'{n}: {v:.5f} +/- {u:.5f}')
