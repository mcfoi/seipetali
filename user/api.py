__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


from .models import User
from common.api import BaseResource
from django.db.models import Avg, Count, F, Max, Min, Sum, Q

class UserResource(BaseResource):

    class Meta(BaseResource.Meta):
        queryset = User.objects.all()
        excludes = [ 'password', 'is_active', 'is_staff', 'is_superuser']


    def build_filters(self, filters=None):
        print 'filters:',filters

        if filters is None:
            filters = {}
        orm_filters = super(UserResource, self).build_filters(filters)

        print 'orm_filters:',orm_filters

        if 'search' in filters:
            query = filters['search']

            qset = reduce(lambda _q,value: _q & (
                Q(first_name__istartswith=value)
                | Q(last_name__istartswith=value)
                | Q(username__icontains=value)
                | Q(email__icontains=value)
            ), query.split(), Q())

            orm_filters.update({'custom': qset})

            print qset

        return orm_filters


    def apply_filters(self, request, applicable_filters):
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None

        semi_filtered = super(UserResource, self).apply_filters(request, applicable_filters)

        return semi_filtered.filter(custom) if custom else semi_filtered



