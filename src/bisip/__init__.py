#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 05-03-2020


from .models import PolynomialDecomposition
from .plotlib import plot_fit, plot_traces


__all__ = [
    'PolynomialDecomposition',
    'plot_fit'
    'plot_traces'
]
