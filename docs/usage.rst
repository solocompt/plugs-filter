=====
Usage
=====

To use Plugs Filter in a project, add it to your `INSTALLED_APPS`:

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
