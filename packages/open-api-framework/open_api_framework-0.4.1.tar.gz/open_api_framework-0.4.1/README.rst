Open API Framework
==================

:Version: 0.4.1
:Source: https://github.com/maykinmedia/open-api-framework
:Keywords: metapackage, dependencies

|build-status| |code-quality| |black| |coverage| |docs|

|python-versions| |django-versions| |pypi-version|

A metapackage for registration components, that bundles the dependencies shared between these components

.. contents::

.. section-numbering::

Features
========

* Bundling shared dependencies and introducing minimum versions for these dependencies

Installation
============

Requirements
------------

* Python 3.9 or above
* Django 4.2 or newer


Install
-------

1. Add open-api-framework to your requirements file
2. Remove dependencies from your requirements file that occur in ``pyproject.toml``
3. Recompile the dependencies

Local development
=================

To install and develop the library locally, use:

.. code-block:: bash

    pip install -e .[tests,coverage,docs,release]

When running management commands via ``django-admin``, make sure to add the root
directory to the python path (or use ``python -m django <command>``):

.. code-block:: bash

    export PYTHONPATH=. DJANGO_SETTINGS_MODULE=testapp.settings
    django-admin check
    # or other commands like:
    # django-admin makemessages -l nl

License
=======

Copyright © Maykin 2024

Licensed under the `MIT license`.


.. _`MIT license`: LICENSE


.. |build-status| image:: https://github.com/maykinmedia/open-api-framework/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/open-api-framework/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/maykinmedia/open-api-framework/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/open-api-framework/actions?query=workflow%3A%22Code+quality+checks%22

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/maykinmedia/open-api-framework/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/open-api-framework
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/open-api-framework/badge/?version=latest
    :target: https://open-api-framework.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/open-api-framework.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/open-api-framework.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/open-api-framework.svg
    :target: https://pypi.org/project/open-api-framework/
