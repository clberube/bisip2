The Inversion Class
===================

Standard usage of :module:`bisip` involves instantiating an
:class:`Inversion` object. This is normally done by invoking one of the
inversion model classes described in the SIP models section below.

.. autoclass:: bisip.models.Inversion
    :members:
    :show-inheritance:

SIP models
----------

.. autoclass:: bisip.models.ColeCole
    :members:
    :show-inheritance:

.. autoclass:: bisip.models.PolynomialDecomposition
    :members:
    :show-inheritance:

Plotting methods
----------------
These functions may be called as methods of the :class:`Inversion` class
after fitting the model to a dataset.

.. autoclass:: bisip.plotlib.plotlib
    :members:

Utility methods
----------------
These utility functions may be called as methods of the :class:`Inversion`
class.

.. autoclass:: bisip.utils.utils
    :members:
