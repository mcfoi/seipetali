__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect,Http404
from django.shortcuts import get_object_or_404
from models import Reservation
from api import ReservationResource

from django.contrib.auth.decorators import login_required

class ReservationDetail(TemplateView):
    template_name = 'reservation/detail.html'




    def get_context_data(self, **kwargs):
        context = {}

        if not kwargs.has_key('pk'):
            raise Http404

        context['reservation'] = get_object_or_404(Reservation, pk=kwargs['pk'])



        res = ReservationResource()
        # res.servizi_opzionali.full = True
        bundle = res.build_bundle(obj=context['reservation'], request=self.request)
        # print bundle
        bundle = res.full_dehydrate(bundle, for_list=True)
        # print bundle

        context['reservation_json'] = res.serialize(None, bundle, "application/json")


        return context


detail = login_required(ReservationDetail.as_view())