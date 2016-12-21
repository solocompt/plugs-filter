"""
Filtering
"""

from django.utils import six
from django.db.models.constants import LOOKUP_SEP

from django_filters import filterset

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
        for name, filter_ in six.iteritems(cls.base_filters.copy()):
            if isinstance(filter_, AutoFilters):
                field = filterset.get_model_field(opts.model, filter_.name)
                filter_exclusion = filter_.extra.pop('drop', [])
                for lookup_expr in utils.lookups_for_field(field):
                    if lookup_expr not in filter_exclusion:
                        new_filter = cls.filter_for_field(field, filter_.name, lookup_expr)
                        filter_name = LOOKUP_SEP.join([name, lookup_expr])
                        cls.base_filters[filter_name] = new_filter

    def __new__(cls, name, bases, attrs):
        """
        Overring the object construction
        """
        new_class = super(Meta, cls).__new__(cls, name, bases, attrs)
        cls.attach_core_filters(new_class)
        return new_class

class FilterSet(six.with_metaclass(Meta, filterset.FilterSet)):
    pass
