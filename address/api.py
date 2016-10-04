__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



from .models import Address


from common.api import BaseResource



class AddressResource(BaseResource):

    class Meta(BaseResource.Meta):
        queryset = Address.objects.all()


#     def hydrate(self, bundle):
#         if not bundle.data.has_key('owner') :
#             bundle.obj.owner = bundle.request.user
#         return bundle
#
#
#
#
#
#
# class ServizioBaseResource(BaseResource):
#
#     class Meta(BaseResource.Meta):
#         queryset = ServizioBase.objects.all()
#
#
#
#
#
# class AlloggioResource(BaseResource):
#
#     class Meta(BaseResource.Meta):
#         queryset = Alloggio.objects.all()
