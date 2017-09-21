"""
Plugs Filter Settings
"""

from django.conf import settings
from django.db.models import fields

PROJECT_SETTINGS = getattr(settings, 'PLUGS_FILTER', {})

DEFAULTS = {
    'LOOKUPS_FOR_FIELDS': {
        fields.related.ForeignKey : ['exact', 'gt', 'lt', 'gte', 'lte', 'in'],
        fields.AutoField : ['exact', 'gt', 'lt', 'gte', 'lte', 'in'],
        fields.IntegerField : ['exact', 'gt', 'lt', 'in'],
        fields.DecimalField : ['exact', 'gt', 'lt', 'in'],
        fields.CharField : ['exact', 'contains', 'icontains', 'in'],
        fields.DateTimeField: ['exact', 'gt', 'lt', 'gte', 'lte'],
        fields.BooleanField: ['exact', 'in'],
        fields.TextField : ['exact', 'contains', 'icontains']
    }
}

try:
    overrides = PROJECT_SETTINGS['LOOKUPS_FOR_FIELDS_OVERRIDES'].items()
    for key, value in overrides:
        DEFAULTS['LOOKUPS_FOR_FIELDS'][key] = value
except KeyError:
    pass

for setting in DEFAULTS.keys():
    if setting not in PROJECT_SETTINGS:
        PROJECT_SETTINGS[setting] = DEFAULTS[setting]

plugs_filter_settings = PROJECT_SETTINGS
