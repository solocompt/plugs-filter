"""
Filters
"""

from django_filters.filters import Filter

class AutoFilters(Filter):
    """
    Automatically adds valid filters for field type
    """
    pass

class DynamicFilters(Filter):
    """
    Creates a list of filters from the passed in attach list
    """
    pass
