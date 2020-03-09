#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   charles
# @Last modified time: 2020-03-09T18:14:23-04:00


import matplotlib.pyplot as plt
from corner import corner


class plotlib:

    def plot_traces(self, chain=None, **kwargs):
        """
        Plots the traces of the MCMC simulation.

        Args:
            chain (:obj:`ndarray`): A numpy array containing the MCMC chain to
                plot. Should have a shape (nwalkers, nsteps, ndim) or
                (nsteps, ndim). If None, the full, unflattened chain will be
                used and all walkers will be plotted. Defaults to None.
            **kwargs: Additional keyword arguments for the get_chain function
                (see below). Use these arguments only if not explicitly passing
                the :obj:`chain` argument.

        Keyword Args:
            discard (:obj:`int`): The number of steps to discard.
            thin (:obj:`int`): The thinning factor (keep every `thin` step).
            flat (:obj:`bool`): Whether to flatten the walkers into a single
                chain or not.

        Returns:
            :obj:`Figure`: A matplotlib figure.

        """
        self.check_if_fitted()
        if chain is None:
            chain = self.get_chain(**kwargs)
        labels = self.param_names
        fig, axes = plt.subplots(self.ndim, figsize=(10, 7), sharex=True)
        for i in range(self.ndim):
            ax = axes[i]
            ax.plot(chain[:, :, i], 'k', alpha=0.3)
            ax.set_xlim(0, len(chain))
            ax.set_ylim(self.bounds[0, i], self.bounds[1, i])
            ax.set_ylabel(labels[i])
            ax.yaxis.set_label_coords(-0.1, 0.5)
        axes[-1].set_xlabel('Steps')
        fig.tight_layout()
        return fig

    def plot_histograms(self, chain=None, bins=25, **kwargs):
        """
        Plots histograms of the MCMC simulation chains.

        Args:
            chain (:obj:`ndarray`): A numpy array containing the MCMC chain to
                plot. Should have a shape (nwalkers, nsteps, ndim) or
                (nsteps, ndim). If None, the full, unflattened chain will be
                used and all walkers will be plotted. Defaults to None.
            bins (:obj:`int`): The number of bins to use in the histograms.
            **kwargs: Additional keyword arguments for the get_chain function
                (see below). Use these arguments only if not explicitly passing
                the :obj:`chain` argument.

        Keyword Args:
            discard (:obj:`int`): The number of steps to discard.
            thin (:obj:`int`): The thinning factor (keep every `thin` step).
            flat (:obj:`bool`): Whether to flatten the walkers into a single
                chain or not.

        Returns:
            :obj:`Figure`: A matplotlib figure.

        """
        self.check_if_fitted()
        chain = self.parse_chain(chain, **kwargs)
        labels = self.param_names
        fig, axes = plt.subplots(self.ndim, figsize=(5, 1.5*chain.shape[1]))
        for i in range(self.ndim):
            ax = axes[i]
            ax.hist(chain[:, i], bins=bins, fc='w', ec='k')
            ax.set_xlabel(labels[i])
            ax.ticklabel_format(axis='x', scilimits=[-2, 2])
        fig.tight_layout()
        return fig

    def plot_fit(self, chain=None, p=[2.5, 50, 97.5], **kwargs):
        """
        Plots the input data, best fit and confidence interval of a model.

        Args:
            chain (:obj:`ndarray`): A numpy array containing the MCMC chain to
                plot. Should have a shape (nwalkers, nsteps, ndim) or
                (nsteps, ndim). If None, the full, unflattened chain will be
                used and all walkers will be plotted. Defaults to None.
            p (:obj:`list` of :obj:`int`): Percentile values for lower
                confidence interval, best fit curve, and upper confidence
                interval, **in that order**. Defaults to [2.5, 50, 97.5] for the
                median and 95% HPD.
            **kwargs: Additional keyword arguments for the get_chain function
                (see below). Use these arguments only if not explicitly passing
                the :obj:`chain` argument.

        Keyword Args:
            discard (:obj:`int`): The number of steps to discard.
            thin (:obj:`int`): The thinning factor (keep every `thin` step).
            flat (:obj:`bool`): Whether to flatten the walkers into a single
                chain or not.

        Returns:
            :obj:`Figure`: A matplotlib figure.

        """
        self.check_if_fitted()
        data = self.data
        lines = self.get_model_percentile(p, chain, **kwargs)
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

    def plot_corner(self, chain, **kwargs):
        """
        Plots the corner plot of the MCMC simulation.

        Args:
            chain (:obj:`ndarray`): A numpy array containing the MCMC chain to
                plot. Should have a shape (nwalkers, nsteps, ndim) or
                (nsteps, ndim). If None, the full, unflattened chain will be
                used and all walkers will be plotted. Defaults to None.
            **kwargs: Additional keyword arguments for the get_chain function
                (see below). Use these arguments only if not explicitly passing
                the :obj:`chain` argument.

        Keyword Args:
            discard (:obj:`int`): The number of steps to discard.
            thin (:obj:`int`): The thinning factor (keep every `thin` step).
            flat (:obj:`bool`): Whether to flatten the walkers into a single
                chain or not.

        Returns:
            :obj:`Figure`: A matplotlib figure.

        """
        self.check_if_fitted()
        fig = corner(chain, labels=self.param_names)
        return fig
