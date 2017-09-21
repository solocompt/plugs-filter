"""
Filtering
"""

from django.utils import six
from django.db.models.constants import LOOKUP_SEP
from django.db import models

from django_filters import filterset, BaseInFilter, ChoiceFilter
from django_filters.utils import try_dbfield
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

    # this is required because we need to override
    # the filter type if it has not_in lookup
    @classmethod
    def filter_for_lookup(cls, f, lookup_type):
        DEFAULTS = dict(cls.FILTER_DEFAULTS)
        if hasattr(cls, '_meta'):
            DEFAULTS.update(cls._meta.filter_overrides)

        data = try_dbfield(DEFAULTS.get, f.__class__) or {}
        filter_class = data.get('filter_class')
        params = data.get('extra', lambda f: {})(f)

        # if there is no filter class, exit early
        if not filter_class:
            return None, {}

        # perform lookup specific checks
        if lookup_type == 'exact' and f.choices:
            return ChoiceFilter, {'choices': f.choices}

        if lookup_type == 'isnull':
            data = try_dbfield(DEFAULTS.get, models.BooleanField)

            filter_class = data.get('filter_class')
            params = data.get('extra', lambda f: {})(f)
            return filter_class, params

        if lookup_type == 'in' or lookup_type == 'not_in':
            class ConcreteInFilter(BaseInFilter, filter_class):
                pass
            ConcreteInFilter.__name__ = cls._csv_filter_class_name(
                filter_class, lookup_type
            )

            return ConcreteInFilter, params

        if lookup_type == 'range':
            class ConcreteRangeFilter(BaseRangeFilter, filter_class):
                pass
            ConcreteRangeFilter.__name__ = cls._csv_filter_class_name(
                filter_class, lookup_type
            )

            return ConcreteRangeFilter, params

        return filter_class, params
