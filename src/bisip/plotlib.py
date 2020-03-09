#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 09-03-2020


import matplotlib.pyplot as plt
from corner import corner


def plot_traces(model, chain=None, **kwargs):
    """
    Plots the traces of the MCMC simulation.

    Args:
        model (:obj:`Inversion`): A fitted Inversion model.
        chain (:obj:`array`): An array containing the MCMC chain to plot.
            Should have a shape (nwalkers, nsteps, ndim) or (nsteps, ndim).
            If None, the full, unflattened chain will be used.
            Defaults to None.
        **kwargs: Additional keyword arguments for the get_chain function
            (see below). Use these arguments only if not explicitly passing a
            `chain` array.

    kwargs:
        discard (:obj:`int`): The number of steps to discard.
        thin (:obj:`int`): The thinning factor (keep every `thin` step).
        flat (:obj:`bool`): Whether to flatten the walkers into a single chain
            or not.

    Returns:
        Figure: A matplotlib.figure.Figure object.

    """
    if chain is None:
        chain = model.get_chain(**kwargs)
    labels = model.param_names
    fig, axes = plt.subplots(model.ndim, figsize=(10, 7), sharex=True)
    for i in range(model.ndim):
        ax = axes[i]
        ax.plot(chain[:, :, i], 'k', alpha=0.3)
        ax.set_xlim(0, len(chain))
        ax.set_ylim(model.bounds[0, i], model.bounds[1, i])
        ax.set_ylabel(labels[i])
        ax.yaxis.set_label_coords(-0.1, 0.5)
    axes[-1].set_xlabel('Steps')
    fig.tight_layout()
    return fig


def plot_histograms(model, chain=None, bins=25, **kwargs):
    chain = model._parse_chain(chain, **kwargs)
    labels = model.param_names
    fig, axes = plt.subplots(model.ndim, figsize=(5, 1.5*chain.shape[1]))
    for i in range(model.ndim):
        ax = axes[i]
        ax.hist(chain[:, i], bins=bins, fc='w', ec='k')
        ax.set_xlabel(labels[i])
        ax.ticklabel_format(axis='x', scilimits=[-2, 2])
    fig.tight_layout()
    return fig


def plot_fit(model, chain=None, p=[2.5, 50, 97.5], **kwargs):
    data = model.data
    lines = model.get_model_percentile(p, chain, **kwargs)
    fig, ax = plt.subplots(2, 1, figsize=(4, 5), sharex=True)
    for i in range(2):
        ax[i].errorbar(data['freq'], data['zn'][i], yerr=data['zn_err'][i],
                       markersize=3, fmt=".k", capsize=0)
        ax[i].plot(data['freq'], lines[0][i], ls=':', c='0.5')
        ax[i].plot(data['freq'], lines[1][i], c='C3')
        ax[i].plot(data['freq'], lines[2][i], ls=':', c='0.5')
        ax[i].set_ylabel(r'$\rho${} (normalized)'.format((i+1)*"'"))
        ax[i].yaxis.set_label_coords(-0.2, 0.5)
    ax[-1].set_xscale('log')
    ax[-1].set_xlabel('$f$ (Hz)')
    fig.tight_layout()
    return fig


def plot_corner(model, chain, **kwargs):
    fig = corner(chain, labels=model.param_names)
    return fig
