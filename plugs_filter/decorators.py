"""
Plugs Core Decorators
"""

from plugs_filter.filters import AutoFilters
from plugs_filter.filtersets import FilterSet

def get_view_model(cls):
    """
    Get the model to use in the filter_class by inspecting
    the queryset or by using a declared auto_filters_model
    """
    msg = 'When using get_queryset you must set a auto_filters_model field in the viewset'
    if cls.queryset is not None:
        return cls.queryset.model
    else:
        assert hasattr(cls, 'auto_filters_model'), msg
        return cls.auto_filters_model

def auto_filters(cls):
    """
    Adds a dynamic filterclass to a viewset
    with all auto filters available for the field type
    that are declared in a tuple auto_filter_fields

    @auto_filters
    def class(...):
        ...
        auto_filters_fields('id', 'location', 'category')
    """
    msg = 'Viewset must have auto_filters_fields set when using auto_filters decorator'
    assert hasattr(cls, 'auto_filters_fields'), msg
    dict_ = {}
    for auto_filter in getattr(cls, 'auto_filters_fields'):
        dict_[auto_filter] = AutoFilters(name=auto_filter)
    # create the inner Meta class and then the filter class
    view_model = get_view_model(cls)
    dict_['Meta'] = type('Meta', (object, ), {'model': view_model, 'fields': ()})
    filter_class = type('DynamicFilterClass', (FilterSet, ), dict_)
    cls.filter_class = filter_class
    return cls
