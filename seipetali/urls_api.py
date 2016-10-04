__author__ = 'elfo'


from django.conf.urls import patterns, include
from tastypie.api import Api



from common.api import *
from seipetali_configuration.api import  IvaResources
from alloggio.api import *
from address.api import *
from reservation.api import *
from user.api import  *

v1_api = Api(api_name='v1')

v1_api.register(PhotoResources())
v1_api.register(GalleryResources())
v1_api.register(IvaResources())

v1_api.register(AlloggioResource())
v1_api.register(ServizioBaseResource())
v1_api.register(ServizioOpzionaleResource())

v1_api.register(AddressResource())
v1_api.register(CalendarResource())
v1_api.register(EventResource())

v1_api.register(ReservationResource())
v1_api.register(PaymentResource())

v1_api.register(UserResource())

def get_urls():
    urlpatterns = patterns('',
        (r'^api/', include(v1_api.urls)),
    )
    return urlpatterns
