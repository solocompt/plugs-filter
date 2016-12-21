"""
Plugs core utils
"""

from django.db.models import fields

LOOKUP_TABLE = {
    # for now we are going to assume that foreign keys are always ints
    fields.related.ForeignKey : ['gt', 'lt', 'gte', 'lte', 'in'],
    fields.AutoField : ['gt', 'lt', 'gte', 'lte', 'in'],
    fields.IntegerField : ['gt', 'lt', 'in'],
    fields.CharField : ['contains', 'icontains'],
    fields.DateTimeField: ['gt', 'lt'],
    fields.BooleanField: ['in'],
    fields.TextField : ['contains', 'icontains']
}

def lookups_for_field(model_field):
    """
    Returns lookups
    """
    return class_lookups(model_field)

def get_field_lookups(field_type, nullable):
    """
    Return lookup table value and append isnull if
    this is a nullable field
    """
    return LOOKUP_TABLE.get(field_type) + ['isnull'] if nullable else LOOKUP_TABLE.get(field_type)

def match_field(field_class):
    """
    Iterates the field_classes and
    returns the first match
    """
    for cls in field_class.mro():
        if cls in list(LOOKUP_TABLE.keys()):
            return cls
    # could not match the field class
    raise Exception('{0} None Found '.format(field_class))

def class_lookups(model_field):
    """
    Return list of available lookups for
    the passed in (model) field type
    """
    field_class = type(model_field)
    field_type = match_field(field_class)
    return get_field_lookups(field_type, model_field.null)
