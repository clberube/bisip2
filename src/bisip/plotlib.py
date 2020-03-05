#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 05-03-2020


import numpy as np
import matplotlib.pyplot as plt


def plot_traces(model, labels):
    fig, axes = plt.subplots(model.ndim, figsize=(10, 7), sharex=True)
    chain = model.get_chain()
    for i in range(model.ndim):
        ax = axes[i]
        ax.plot(chain[:, :, i], 'k', alpha=0.3)
        ax.set_xlim(0, len(chain))
        ax.set_ylabel(labels[i])
        ax.yaxis.set_label_coords(-0.1, 0.5)
    axes[-1].set_xlabel('Steps')
    fig.tight_layout()

    return fig


def plot_fit(model, chain=None, **kwargs):

    if chain is None:
        # if discard is not None and thin is not None:
        kwargs['flat'] = True
        chain = model.get_chain(**kwargs)

    else:
        if chain.ndim > 2:
            raise ValueError('Flatten chain before passing to plot_fit().')

        if 'discard' in kwargs or 'thin' in kwargs:
            raise ValueError('Please pass either a chain obtained with '
                             'the get_chain() method or pass '
                             'discard and thin keywords to plot_fit(). '
                             'Do not pass both arguments.')

    fig, ax = plt.subplots(2, 1, figsize=(4, 5), sharex=True)
    data = model.data
    best = model.forward(np.median(chain, axis=0), data['w'])
    low = model.forward(np.percentile(chain, 2.5, axis=0), data['w'])
    high = model.forward(np.percentile(chain, 97.5, axis=0), data['w'])

    for i in range(2):
        ax[i].errorbar(data['freq'], data['zn'][i],
                       yerr=data['zn_err'][i], fmt=".k", capsize=0)
        ax[i].plot(data['freq'], best[i], c='C3')
        ax[i].plot(data['freq'], low[i], ls=':', c='0.5')
        ax[i].plot(data['freq'], high[i], ls=':', c='0.5')
        ax[i].set_ylabel(r'$\rho${} (normalized)'.format((i+1)*"'"))
        ax[i].yaxis.set_label_coords(-0.2, 0.5)

    ax[-1].set_xscale('log')
    ax[-1].set_xlabel('$f$ (Hz)')
    fig.tight_layout()

    return fig
