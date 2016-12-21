"""
Solo Core Decorators
"""
from solo.core.filters import AutoFilters
from solo.core.filtersets import FilterSet

def get_view_model(cls):
    """
    Get the model to use in the filter_class by inspecting
    the queryset or by using a declared auto_filters_model
    """
    if cls.queryset is not None:
        return cls.queryset.model
    else:
        assert cls.auto_filters_model, 'if using get_queryset you must set a auto_filters_model field in the viewset'
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
    if hasattr(cls, 'auto_filters_fields'):
        dict_ = {}
        for auto_filter in getattr(cls, 'auto_filters_fields'):
            dict_[auto_filter] = AutoFilters(name=auto_filter)
        # create the inner Meta class and then the filter class
        view_model = get_view_model(cls)
        dict_['Meta'] = type('Meta', (object, ), {'model': view_model, 'fields': ()})
        filter_class = type('DynamicFilterClass', (FilterSet, ), dict_)
        cls.filter_class = filter_class
    return cls

def decorator_factory(message, attr):
    """
    Factory to create CUD decorators
    """
    def decorator(func):
        """
        Attach decorator
        """
        setattr(func, attr, True)
        func.message = message
        return func
    return decorator

def deletable(message=None):
    """
    Marks a method has deletable
    the marked method will be called on
    model delete, requires the CUD mixin
    """
    message = 'Cannot Delete' if (message is None) else message
    attr = '__deletable'
    return decorator_factory(message, attr)

def creatable(message=None):
    """
    Marks a method has creatable
    the marked method will be called on
    model save if the object has no pk,
    requires the CUD mixin
    """
    message = 'Cannot Create' if (message is None) else message
    attr = '__creatable'
    return decorator_factory(message, attr)

def updatable(message=None):
    """
    Marks a method has updatable
    the marked method will be called on
    model save if the object has pk,
    requires the CUD mixin
    """
    message = 'Cannot Update' if (message is None) else message
    attr = '__updatable'
    return decorator_factory(message, attr)
