.. _install:

Installation
============

BISIP is compatible with Python 3.7.
You will also need the following packages:

- `numpy <https://numpy.org/>`_
- `matplotlib <https://matplotlib.org/>`_
- `emcee <https://emcee.readthedocs.io/en/stable/>`_

And optionally the corner package to draw corner plots:

- `corner <https://corner.readthedocs.io/en/latest/>`_

Package managers
----------------

TODO

From source
-----------

BISIP is developed on `GitHub <https://github.com/clberube/bisip2>`_.
Clone the repository to your computer.
Then navigate to the bisip directory.
Finally run the setup.py script with Python.

.. code-block:: bash

  git clone https://github.com/clberube/bisip2
  cd bisip2
  python setup.py install -f

Testing
-----------

To test if everything was installed correctly, do the following:

.. code-block:: python

  # Last tested on Python 3.7.3 (default, Mar 27 2019, 16:54:48)
  import bisip
  bisip.run_test()

If everything is OK the code will load a data file and perform ColeCole
and Debye decomposition of a data file, then print the best parameters and
plot traces and fit quality for the decomposition approach. Then you should
see the following line:

.. code-block::

    All tests passed. Press ctrl+C or close figure windows to exit.
