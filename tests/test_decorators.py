"""
Testing Decorators
"""

from django.db import models
from django.test import TestCase

from rest_framework import viewsets

from plugs_filter.decorators import auto_filters
from plugs_filter.filtersets import Meta
from plugs_filter.utils import LOOKUP_TABLE

class TestModel(models.Model):
    charfield = models.CharField(max_length=100)
    integerfield = models.IntegerField()

    class Meta:
        app_label = 'plugs_filter'


class TestDecorators(TestCase):
    """
    Testing Decorators
    """

    def test_assertion_when_auto_filters_fields_missing(self):
        """
        Ensures assertion when auto_filters_fields is missing from viewset
        """
        msg = 'Viewset must have auto_filters_fields set when using auto_filters decorator'
        with self.assertRaisesMessage(AssertionError, msg):
            @auto_filters
            class TestViewSet(viewsets.ModelViewSet):
                pass


    def test_assertion_when_auto_filters_model_missing(self):
        """
        Ensures assertion when auto_filters_model is missing from a viewset without queryset
        """
        msg = 'When using get_queryset you must set a auto_filters_model field in the viewset'
        with self.assertRaisesMessage(AssertionError, msg):
            @auto_filters
            class TestViewSet(viewsets.ModelViewSet):
                auto_filters_fields = ('field', )

                def get_queryset(self):
                    return None


    def test_metaclass_used_to_create_filterclass(self):
        """
        Ensures auto filters metaclass used to create filterclass
        """
        @auto_filters
        class TestViewSet(viewsets.ModelViewSet):
            queryset = TestModel.objects.all()
            auto_filters_fields = ('charfield', 'integerfield')

        self.assertIsInstance(TestViewSet.filter_class, Meta)


    def test_default_lookup_fields_for_charfield(self):
        """
        Ensures default lookup fields for charfield
        """
        @auto_filters
        class TestViewSet(viewsets.ModelViewSet):
            queryset = TestModel.objects.all()
            auto_filters_fields = ('charfield', )

        base_filters = TestViewSet.filter_class.base_filters
        for lookup_expr in LOOKUP_TABLE[models.fields.CharField]:
            self.assertIn('charfield__' + lookup_expr, base_filters)
