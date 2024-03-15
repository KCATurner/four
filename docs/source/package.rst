################
Package Contents
################

.. currentmodule:: four

Four contains three submodules written primarily to support the CLI.

.. autosummary::
    :toctree: package

    chain
    graph
    infer

And for any other lost souls out there with nothing better to do, I've
attempted to organize an API you can use to have your own "fun"
exploring 4-chains. While API members are seperated into three main
'private' submodules for organizational purposes, any documented API
member can be imported directly from the package root.

.. code-block:: python

    >>> from four import PNumber
    >>> # is the same as...
    >>> from four._oo_api import PNumber

However, before reading further about API members, it may be wise to
familiarize yourself with some common concepts and terminology used
throughout the API documentation. :math:`\ `

.. autosummary::
    :toctree: package

    _core
    _fp_api
    _oo_api
