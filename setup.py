#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cberube
# @Date:   05-03-2020
# @Email:  charles@goldspot.ca
# @Last modified by:   cberube
# @Last modified time: 05-03-2020
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 16:18:50 2017

@author: Charles
"""

from setuptools import setup, find_packages

from distutils.core import setup
from distutils.extension import Extension
from distutils.command.sdist import sdist as _sdist
import numpy

class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        from Cython.Build import cythonize
        cythonize(['./src/bisip/cython_funcs.pyx'])
        _sdist.run(self)

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

cmdclass = { }
ext_modules = [ ]

cmdclass['sdist'] = sdist

if use_cython:
    ext_modules += [
        Extension("bisip.cython_funcs", [ "./src/bisip/cython_funcs.pyx" ]),
    ]
    cmdclass.update({ 'build_ext': build_ext })
    print("up")
else:
    ext_modules += [
        Extension("bisip.cython_funcs", [ "./src/bisip/cython_funcs.c" ],
                  include_dirs=[numpy.get_include()]),
    ]
    print("down")

setup(
  name = 'bisip2',
  packages=['bisip2',], # this must be the same as the name above
  # py_models=['models','invResults','GUI'],
  version = '0.0.1',
  license = 'MIT',
  install_requires=['emcee', 'numpy', 'matplotlib'],
  description = 'Bayesian inversion of SIP data',
  long_description = 'README.md',
  author = 'Charles L. Berube',
  author_email = 'charleslberube@gmail.com',
  url = 'https://github.com/clberube/bisip2', # use the URL to the github repo
#  download_url = 'https://github.com/clberube/BISIP/archive/0.0.1.tar.gz', # I'll explain this in a second
  keywords = ['stochastic inversion','spectral induced polarization','mcmc'], # arbitrary keywords
  classifiers = [],
  cmdclass = cmdclass,
  ext_modules = ext_modules,
  include_dirs=[numpy.get_include()],
)
