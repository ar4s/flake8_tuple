============
flake8_tuple
============

.. image:: https://img.shields.io/travis/ar4s/flake8_tuple.svg
        :target: https://travis-ci.org/ar4s/flake8_tuple

.. image:: https://img.shields.io/pypi/v/flake8_tuple.svg
        :target: https://pypi.python.org/pypi/flake8_tuple


A flake8_tuple plugin checks for (probably) unintended one element tuples like::

    foo = 123,

Install
--------

Install with ``pip``::

    $ pip install flake8-tuple

You can check that ``flake8`` has picked it up by looking for ``flake8-tuple``
in the output of ``--version``:

.. code-block:: sh

    $ flake8 --version
    2.6.2 (pycodestyle: 2.0.0, flake8-tuple: 0.2.10, pyflakes: 1.2.3, mccabe: 0.5.0) CPython 2.7.11+ on Linux



Warnings
--------

This plugin add new flake8 warning:

- ``T801``: one element tuple.


Requirements
-------------

* Python 2.x, 3.x (tested on 2.7, 3.4, 3.5, 3.6 and 3.7)
* flake8 or pycodestyle


Licence
-------

BSD license
