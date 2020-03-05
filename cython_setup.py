#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   03-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 05-03-2020


try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("./src/bisip/cython_funcs.pyx"),
    include_dirs=[numpy.get_include()]
)
