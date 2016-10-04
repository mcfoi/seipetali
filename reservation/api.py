__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from models import Reservation,ReservationService,Payment
from common.api import BaseResource,MyAuthorization
from tastypie import fields
from tastypie.authorization import Authorization,Unauthorized
import sys
from tastypie.constants import ALL, ALL_WITH_RELATIONS

class ReservationAuthorization(MyAuthorization):
    #
    # def read_list(self, object_list, bundle):
    #     # print "%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
    #     # print bundle.request.user
    #     # This assumes a ``QuerySet`` from ``ModelResource``.
    #     return object_list
    #
    # def read_detail(self, object_list, bundle):
    #     # print("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
    #     # print bundle.request.user
    #     # Is the requested object owned by the user?
    #     return True
    #
    # def create_list(self, object_list, bundle):
    #     print("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
    #     # Assuming they're auto-assigned to ``user``.
    #     if bundle.request.user.is_superuser:
    #         return object_list
    #     else:
    #         raise Unauthorized("Sorry, you're not superuser.")
    #
    # def create_detail(self, object_list, bundle):
    #     print("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
    #     print bundle.request.user
    #     if bundle.request.user.is_superuser:
    #         return True
    #     else:
    #         raise Unauthorized("Sorry, you're not superuser.")
    #
    # def update_list(self, object_list, bundle):
    #     # print ("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
    #     allowed = []
    #     #
    #     # # Since they may not all be saved, iterate over them.
    #     # for obj in object_list:
    #     #     if obj in bundle.request.user.brandManaged:
    #     #         allowed.append(obj)
    #     #
    #     # return allowed
    #     if bundle.request.user.is_superuser:
    #         return object_list
    #     else:
    #         return allowed
    #
    # def update_detail(self, object_list, bundle):
    #     # print("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
    #
    #     if bundle.request.user.is_superuser:
    #         return True
    #     else:
    #         raise Exception('Sorry, you are not   admin. ')
    #         # raise Unauthorized("Sorry, you are not  brand admin.")
    #     # return bundle.obj.user == bundle.request.user
    #
    def delete_list(self, object_list, bundle):
        # print ("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        print ("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
        print bundle.request.user , object_list,bundle.obj.id
        # raise Unauthorized("Sorry, no deletes.")

        if bundle.request.user.is_staff:
            return True
        else:
            raise Unauthorized("Sorry, no deletes.")


class ReservationResource(BaseResource):

    event = fields.ForeignKey('common.api.EventResource','event',full=True,null=True,blank=True,readonly=True)
    servizi_opzional = fields.OneToManyField('reservation.api.ReservationServiceResource','servizi_opzional',full=True,)
    payments = fields.OneToManyField('reservation.api.PaymentResource','payment_set',full=True,)
    user = fields.ForeignKey('user.api.UserResource','user',full=True,null=True,blank=True,readonly=True)

    class Meta(BaseResource.Meta):
        queryset = Reservation.objects.all()
        allowed_methods = ['get', 'post', 'patch','delete']
        authorization = ReservationAuthorization()
        filtering = {
            # "id": ALL,
            "user": ALL_WITH_RELATIONS
            # "student": ALL_WITH_RELATIONS,
            # 'archived': ALL
        }

class ReservationServiceResource(BaseResource):

    class Meta(BaseResource.Meta):
        queryset = ReservationService.objects.all()


class PaymentResource(BaseResource):
    reservation = fields.ForeignKey('reservation.api.ReservationResource','reservation',full=False,null=False,blank=False)

    class Meta(BaseResource.Meta):
        queryset = Payment.objects.all()
        allowed_methods = ['get', 'post','delete']


