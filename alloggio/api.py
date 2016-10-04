__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from tastypie import fields
from .models import ServizioBase,ServizioOpzionale,Alloggio
from django.conf.urls import  url
from tastypie.resources import trailing_slash,http,ObjectDoesNotExist,MultipleObjectsReturned
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from common.api import BaseResource
import dateutil.parser
from exceptions import AlloggioInvalidTimeslot,AlloggioNotActive,AlloggioUnavailable
from tastypie import http
from django.http import HttpResponseRedirect
from importlib import import_module
from django.conf import settings
from django.core.urlresolvers import reverse
from address.models import Address

class ServizioOpzionaleResource(BaseResource):

    class Meta(BaseResource.Meta):
        queryset = ServizioOpzionale.objects.all()


    def hydrate(self, bundle):
        if not bundle.data.has_key('owner') :
            bundle.obj.owner = bundle.request.user
        return bundle






class ServizioBaseResource(BaseResource):

    class Meta(BaseResource.Meta):
        queryset = ServizioBase.objects.all()





class AlloggioResource(BaseResource):

    address = fields.ForeignKey('address.api.AddressResource','address',full=True,null=True,blank=True)
    events = fields.ManyToManyField('common.api.EventResource','events',full=False,null=True,blank=True,readonly=True)
    calendar = fields.ForeignKey('common.api.CalendarResource','calendar',full=False,null=True,blank=True,readonly=True)
    gallery = fields.ForeignKey('common.api.GalleryResources','gallery',full=False,null=True,blank=True,readonly=True)
    servizi_opzionali = fields.ManyToManyField('alloggio.api.ServizioOpzionaleResource','servizi_opzionali',null=True,blank=True,readonly=True)
    owner = fields.ForeignKey('user.api.UserResource','owner',full=False,null=True,blank=True)

    class Meta(BaseResource.Meta):
        queryset = Alloggio.objects.all()
        filtering = {
            "id": ALL,
            "active": ALL,
            "owner": ALL_WITH_RELATIONS,
            # 'archived': ALL
        }



    def prepend_urls(self):
        # print "ResourceName:" + self._meta.resource_name
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/quote%s$" % (self._meta.resource_name,trailing_slash()), self.wrap_view('get_quote'), name="api_alloggio_quote"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/book%s$" % (self._meta.resource_name,trailing_slash()), self.wrap_view('book'), name="api_alloggio_book"),


        ]




    def apply_filters(self, request, applicable_filters):

        query_start = request.GET.get('start', None)
        query_end = request.GET.get('end', None)
        query_numero_ospiti = request.GET.get('numero_ospiti', None)


        bounds_ne_lat = request.GET.get('bounds_ne_lat', None)
        bounds_ne_lng = request.GET.get('bounds_ne_lng', None)
        bounds_sw_lat = request.GET.get('bounds_sw_lat', None)
        bounds_sw_lng = request.GET.get('bounds_sw_lng', None)





        if query_start and query_end:
            base_object_list = Alloggio.objects.filter_free_for_date(query_start,query_end)
        else:
            base_object_list = self.get_object_list(request)

        if query_numero_ospiti:
            base_object_list = base_object_list.filter(postiletto__gte=query_numero_ospiti)


        if bounds_ne_lat and bounds_sw_lat and bounds_ne_lng and bounds_sw_lng:
            try:
                valid_address_id = Address.objects.filter(latitude__range=(float(bounds_sw_lat),float(bounds_ne_lat))).filter(longitude__range=(float(bounds_sw_lng),float(bounds_ne_lng))).values_list('id', flat=True)
                base_object_list = base_object_list.filter(address__in=valid_address_id)
            except Exception as e:
                print e


        base_object_list = base_object_list.filter(**applicable_filters)

        return base_object_list



    def parseQuoteReservetionRequest(self, request, **kwargs):
        print 'parseQuoteReservetionRequest:',kwargs
        # basic_bundle = self.build_bundle(request=request)
        query_start = request.GET.get('start', None)
        query_end = request.GET.get('end', None)
        query_numero_ospiti = request.GET.get('numero_ospiti', None)

        query_servizi_opzionali = request.GET.getlist('servizi_opzionali', None)


        if isinstance(query_start,str) or isinstance(query_start,unicode):
            query_start = dateutil.parser.parse(query_start)

        if isinstance(query_end,str) or isinstance(query_end,unicode):
            query_end = dateutil.parser.parse(query_end)


        if query_start and query_end:
            base_object_list = Alloggio.objects.filter_free_for_date(query_start,query_end)
        else:
            raise AlloggioInvalidTimeslot
            # print 'Check-in Check-Out non setted'
            # return http.HttpBadRequest('Check-in Check-Out non setted')
            # return self.create_response(request,data={'error_message':'Check-in Check-Out non setted'},response_class=http.HttpBadRequest)
            # raise Exception('Check-in Check-Out non setted')
            # base_object_list = self.get_object_list(request)

        if query_numero_ospiti:
            base_object_list = base_object_list.filter(postiletto__gte=query_numero_ospiti)



        try:
            # obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
            obj =  base_object_list.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            raise AlloggioUnavailable
            # raise Exception('Alloggio non disponibile')
            # return self.create_response(request,data={'error_message':'Alloggio non disponibile'},response_class=http.HttpNotFound)
        except MultipleObjectsReturned:
            raise MultipleObjectsReturned
            # print 'MultipleObjectsReturned'
            # return self.create_response(request,data={'error_message':'More than one resource is found at this URI.'},response_class=http.HttpMultipleChoices)
            # return http.HttpMultipleChoices("More than one resource is found at this URI.")


        if not obj.active:
            raise AlloggioNotActive
            # raise Exception('Alloggio non piu in affitto')



        servizi_opzionali = []
        if query_servizi_opzionali:
            res = ServizioOpzionaleResource()
            for uri in query_servizi_opzionali:
                try:
                    servizi_opzionali.append(res.get_via_uri(uri))
                except:
                    pass


        bundle = self.build_bundle(obj=obj, request=request)

        quote_params = {
            'start' : query_start,
            'end': query_end,
            'numero_ospiti': query_numero_ospiti,
            'servizi_opzionali': servizi_opzionali
        }

        return bundle,quote_params


    def book(self, request, **kwargs):
        # print 'Book'


        try:
            bundle,quote_params = self.parseQuoteReservetionRequest(request, **kwargs)
        except AlloggioNotActive:
            raise Exception('Alloggio non piu in affitto')
        except AlloggioUnavailable:
            return self.create_response(request,data={'error_message':'Alloggio non disponibile'},response_class=http.HttpNotFound)
        except AlloggioInvalidTimeslot:
            return self.create_response(request,data={'error_message':'Check-in Check-Out non setted'},response_class=http.HttpBadRequest)

        quote_params['user'] = request.user
        quote_params['session'] = request.session

        reservation = bundle.obj.book(**quote_params)

        if reservation:
            if request.user.is_anonymous():
                request.session['reservation_id'] = reservation.id

            bundle.data['redirect_url'] = reverse('reservation_detail', kwargs={'pk':reservation.pk})
            return self.create_response(request, bundle)

        return self.create_response(request, bundle)





    def get_quote(self, request, **kwargs):

        # # basic_bundle = self.build_bundle(request=request)
        # query_start = request.GET.get('start', None)
        # query_end = request.GET.get('end', None)
        # query_numero_ospiti = request.GET.get('numero_ospiti', None)
        #
        # query_servizi_opzionali = request.GET.getlist('servizi_opzionali', None)
        #
        #
        # if isinstance(query_start,str) or isinstance(query_start,unicode):
        #     query_start = dateutil.parser.parse(query_start)
        #
        # if isinstance(query_end,str) or isinstance(query_end,unicode):
        #     query_end = dateutil.parser.parse(query_end)
        #
        #
        # if query_start and query_end:
        #     base_object_list = Alloggio.objects.filter_free_for_date(query_start,query_end)
        # else:
        #     # return http.HttpBadRequest('Check-in Check-Out non setted')
        #     return self.create_response(request,data={'error_message':'Check-in Check-Out non setted'},response_class=http.HttpBadRequest)
        #     # raise Exception('Check-in Check-Out non setted')
        #     # base_object_list = self.get_object_list(request)
        #
        # if query_numero_ospiti:
        #     base_object_list = base_object_list.filter(postiletto__gte=query_numero_ospiti)
        #
        #
        #
        # try:
        #     # obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        #     obj =  base_object_list.get(id=kwargs['pk'])
        # except ObjectDoesNotExist:
        #     # raise Exception('Alloggio non disponibile')
        #     return self.create_response(request,data={'error_message':'Alloggio non disponibile'},response_class=http.HttpNotFound)
        # except MultipleObjectsReturned:
        #     return self.create_response(request,data={'error_message':'More than one resource is found at this URI.'},response_class=http.HttpMultipleChoices)
        #     # return http.HttpMultipleChoices("More than one resource is found at this URI.")
        #
        #
        # if not obj.active:
        #     raise Exception('Alloggio non piu in affitto')
        #
        #
        #
        # servizi_opzionali = []
        # if query_servizi_opzionali:
        #     res = ServizioOpzionaleResource()
        #     for uri in query_servizi_opzionali:
        #         try:
        #             servizi_opzionali.append(res.get_via_uri(uri))
        #         except:
        #             pass
        #
        #
        # bundle = self.build_bundle(obj=obj, request=request)
        #
        # quote_params = {
        #     'start' : query_start,
        #     'end': query_end,
        #     'numero_ospiti': query_numero_ospiti,
        #     'servizi_opzionali': servizi_opzionali
        # }

        # bundle,quote_params = self.parseQuoteReservetionRequest(request, **kwargs)
        try:
            bundle,quote_params = self.parseQuoteReservetionRequest(request, **kwargs)
        except AlloggioNotActive:
            raise Exception('Alloggio attualmente non in affitto')
        except AlloggioUnavailable:
            return self.create_response(request,data={'error_message':'Alloggio non disponibile'},response_class=http.HttpNotFound)
        except AlloggioInvalidTimeslot:
            return self.create_response(request,data={'error_message':'Check-in Check-Out non setted'},response_class=http.HttpBadRequest)

        try:
            bundle.data = bundle.obj.getQuote(**quote_params)
        except Exception as e:
            return self.create_response(request,data={'error_message':e.message},response_class=http.HttpBadRequest)
        # bundle = self.full_dehydrate(bundle)
        # bundle = self.alter_detail_data_to_serialize(request, bundle)

        print bundle
        # message = 'Approve Lesson'
        # action = lesson.RESERVATION_APPROVED
        #
        # lesson.update(request.user,message,action,request)
        # newLesson = Lesson.objects.get(id=lesson.id)

        # bundle = self.build_bundle(obj=alloggio, request=request)
        # bundle = self.full_dehydrate(bundle)

        return self.create_response(request, bundle)