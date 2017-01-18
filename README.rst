=============================
Plugs Filter
=============================

.. image:: https://badge.fury.io/py/plugs-filter.png
    :target: https://badge.fury.io/py/plugs-filter

.. image:: https://travis-ci.org/ricardolobo/plugs-filter.png?branch=master
    :target: https://travis-ci.org/ricardolobo/plugs-filter

Your project description goes here

Documentation
-------------

The full documentation is at https://plugs-filter.readthedocs.io.

Quickstart
----------

Install Plugs Filter::

    pip install plugs-filter

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'plugs_filter.apps.PlugsFilterConfig',
        ...
    )

Add Plugs Filter's URL patterns:

.. code-block:: python

    from plugs_filter import urls as plugs_filter_urls


    urlpatterns = [
        ...
        url(r'^', include(plugs_filter_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
