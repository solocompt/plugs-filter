from django.db.models.lookups import In
from django.db.models.fields import Field

@Field.register_lookup
class NotIn(In):
    lookup_name = 'not_in'

    def get_rhs_op(self, connection, rhs):
        return 'NOT IN %s' % rhs
