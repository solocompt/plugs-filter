"""
Filtering
"""

from django.utils import six
from django.db.models.constants import LOOKUP_SEP

from django_filters import filterset
from django_filters.rest_framework.filterset import FilterSet as RESTFrameworkFilterSet

from plugs_filter.filters import AutoFilters
from plugs_filter import utils

class Meta(filterset.FilterSetMetaclass):
    """
    Metaclass for Filtersets

    How AutoFilters are declared:
    def SomeFilterClass(FilterSet):
        location = AutoFilters(name='location')
        class Meta:
            model = models.Experience
            fields = ()

    Optionally you can drop some of the default
    auto filters by using drop

    ...
        location = AutoFilters(name='location', drop=['in', 'gte'])
    ...
    """

    def attach_core_filters(cls):
        """
        Attach core filters to filterset
        """
        opts = cls._meta
        base_filters = cls.base_filters.copy()
        cls.base_filters.clear()
        for name, filter_ in six.iteritems(base_filters):
            if isinstance(filter_, AutoFilters):
                field = filterset.get_model_field(opts.model, filter_.name)
                filter_exclusion = filter_.extra.pop('drop', [])
                for lookup_expr in utils.lookups_for_field(field):
                    if lookup_expr not in filter_exclusion:
                        new_filter = cls.filter_for_field(field, filter_.name, lookup_expr)
                        # by convention use field name for filters with exact lookup_expr
                        if lookup_expr != 'exact':
                            filter_name = LOOKUP_SEP.join([name, lookup_expr])
                        else:
                            filter_name = name
                        cls.base_filters[filter_name] = new_filter

    def __new__(cls, name, bases, attrs):
        """
        Overring the object construction
        """
        new_class = super(Meta, cls).__new__(cls, name, bases, attrs)
        cls.attach_core_filters(new_class)
        return new_class

class FilterSet(six.with_metaclass(Meta, RESTFrameworkFilterSet)):
    pass
