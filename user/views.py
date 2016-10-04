__author__ = 'elfo'
# -*- coding: utf-8 -*-

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from .models import User
from .forms import LocatoreForm
from  django.views.generic import UpdateView

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from common.utils import get_cms_page_url


class RegistraLocatoreView(UpdateView):
    template_name = 'user/locatore_form.html'
    model = User
    form_class = LocatoreForm
    # success_url = reverse('alloggio_create')


    def get_form_kwargs(self):
        kwargs = super(RegistraLocatoreView,self).get_form_kwargs()

        kwargs['terms_url'] = get_cms_page_url('terms',request=self.request)
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('alloggio_create')

    def form_valid(self, form):
        self.request.user.locatore = True
        self.request.user.save()
        return super(RegistraLocatoreView,self).form_valid(form)


registra_locatore = login_required(RegistraLocatoreView.as_view())