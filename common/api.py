__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# from sorl.thumbnail import get_thumbnail

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS,dict_strip_unicode_keys,http
from tastypie import fields
from tastypie.authentication import SessionAuthentication,MultiAuthentication,Authentication
from tastypie.authorization import Authorization
from django.conf.urls import url
from tastypie.utils import trailing_slash
# from models import *
from tastypie.serializers import Serializer
from django.http.request import RawPostDataException

import sys
from tastypie.exceptions import Unauthorized
from tastypie.http import HttpUnauthorized
# from click.models import Click

from photologue.models import Photo,Gallery
from schedule.models import Calendar,Event,Occurrence
from datetime import datetime
from django.utils.text import slugify


class MyAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        # print "%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name)
        # print bundle.request.user
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list

    def read_detail(self, object_list, bundle):
        # print("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
        # print bundle.request.user
        # Is the requested object owned by the user?
        return True

    def create_list(self, object_list, bundle):
        print("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
        # Assuming they're auto-assigned to ``user``.
        if bundle.request.user.is_superuser:
            return object_list
        else:
            raise Unauthorized("Sorry, you're not superuser.")

    def create_detail(self, object_list, bundle):
        print("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
        print bundle.request.user
        if bundle.request.user.is_superuser or bundle.request.user.is_staff or bundle.request.user.isLocatore() :
            return True
        else:
            raise Unauthorized("Sorry, you're not superuser.")

    def update_list(self, object_list, bundle):
        # print ("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
        allowed = []
        #
        # # Since they may not all be saved, iterate over them.
        # for obj in object_list:
        #     if obj in bundle.request.user.brandManaged:
        #         allowed.append(obj)
        #
        # return allowed
        if bundle.request.user.is_superuser or bundle.request.user.is_staff or bundle.request.user.isLocatore() :
            return object_list
        else:
            return allowed

    def update_detail(self, object_list, bundle):
        # print("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))

        if bundle.request.user.is_superuser or bundle.request.user.isLocatore()  or bundle.request.user.isLocatore():
            return True
        else:
            raise Exception('Sorry, you are not admin. ')
            # raise Unauthorized("Sorry, you are not  brand admin.")
        # return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # print ("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        # print ("%s - %s" % (self.__class__.__name__, sys._getframe().f_code.co_name))
        if bundle.request.user.is_superuser or bundle.request.user.isLocatore()  or bundle.request.user.is_staff:
            return True
        else:
            raise Unauthorized("Sorry, no deletes.")

class BaseResource(ModelResource):

    class Meta:
        authorization = MyAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(),Authentication())
        include_resource_uri = True
        list_allowed_methods = ['get','post']
        allowed_methods = ['get', 'post', 'patch']
        always_return_data = True
        serializer = Serializer()

    def post_list(self, request, **kwargs):
        """
        Creates a new resource/object with the provided data.

        Calls ``obj_create`` with the provided data and returns a response
        with the new resource's location.

        If a new resource is created, return ``HttpCreated`` (201 Created).
        If ``Meta.always_return_data = True``, there will be a populated body
        of serialized data.
        """
        print 'postList'
        try:
            deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        except RawPostDataException as e:

            print request
            deserialized = self.deserialize(request, request.raw_request_data,
                                    format=request.META.get('CONTENT_TYPE', 'application/json'))
            print e, type(e)

        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
        location = self.get_resource_uri(updated_bundle)

        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)


    def post_detail(self, request, **kwargs):
        return super(BaseResource, self).patch_detail(request, **kwargs)

    def deserialize(self, request, data, format=None):
        print 'DESERIALIZE'
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data

        return super(BaseResource, self).deserialize(request, data, format)




class PhotoResources(BaseResource):




    class Meta(BaseResource.Meta):
        queryset = Photo.objects.all()



    def dehydrate(self, bundle):
        if not bundle.data.has_key('image_url'):
            bundle.data['image_url'] = bundle.obj.image.url

        bundle.data['thumbnail_url'] = bundle.obj.get_thumbnail_url()
        return bundle

    def hydrate(self, bundle):
        print 'PhotoResources hydrate'
        if not bundle.data.has_key('title') and bundle.data.has_key('image'):
            bundle.data['title'] = datetime.now().strftime("%Y%m%d-%H%M%S") + bundle.data['image'].name
            bundle.data['slug'] = slugify(bundle.data['title'])
        return bundle


    def obj_create(self,bundle,**kwargs):
        bundle = super(PhotoResources,self).obj_create(bundle,**kwargs)

        # Add code here
        print 'Photo created....'

        return bundle


class GalleryResources(BaseResource):


    photos = fields.ManyToManyField('common.api.PhotoResources','photos',full=True,null=True,blank=True)

    class Meta(BaseResource.Meta):
        queryset = Gallery.objects.all()



    def hydrate(self, bundle):
        if not bundle.data.has_key('title') :
            bundle.data['title'] = u''+datetime.now().strftime("%Y%m%d-%H%M%S")
            bundle.data['slug'] = slugify(bundle.data['title'])
        return bundle



class CalendarResource(BaseResource):
    alloggio = fields.ForeignKey('alloggio.api.AlloggioResource','alloggio')

    class Meta(BaseResource.Meta):
        queryset = Calendar.objects.all()
        filtering = {
            "alloggio": ALL_WITH_RELATIONS,
            # "student": ALL_WITH_RELATIONS,
            # 'archived': ALL
        }

class EventResource(BaseResource):
    calendar = fields.ForeignKey('common.api.CalendarResource','calendar')

    reservation = fields.OneToManyField('reservation.api.ReservationResource','reservation_set',full=False,null=True,blank=True,readonly=True)

    class Meta(BaseResource.Meta):
        queryset = Event.objects.all()
        filtering = {
            'start': ALL,
            'end': ALL,
            "calendar": ALL_WITH_RELATIONS,
            # "student": ALL_WITH_RELATIONS,
        }
        allowed_methods = ['get', 'post', 'patch','delete']


    def dehydrate(self, bundle):
        bundle.data['color'] = '#000'
        if bundle.obj.reservation_set.count():
            bundle.data['color'] = '#3ABD77'
        return  bundle

    # def apply_filters(self, request, applicable_filters):
    #     base_object_list = super(EventResource, self).apply_filters(request, applicable_filters)
    #
    #     query = request.GET.get('mylessons', None)
    #
    #     if query:
    #         queryset = (
    #             Q(student__id=query) |
    #             Q(teacher__id=query)
    #         )
    #         base_object_list = base_object_list.filter(queryset).distinct()
    #
    #     return base_object_list
