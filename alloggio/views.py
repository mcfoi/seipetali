__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.contrib.auth.decorators import login_required,permission_required
from django.core import urlresolvers
from django.conf import settings
from  django.views.generic import TemplateView,CreateView,UpdateView
from django.views.generic.edit import ModelFormMixin
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from .models import Alloggio
from address.forms import FullAddressForm
from forms import AlloggioForm,BaseSearchForm
from django.contrib.auth.decorators import login_required
from api import AlloggioResource
from common.api import GalleryResources


from django.core.mail import send_mail



class AlloggioList(TemplateView):
    template_name = 'alloggio/list.html'



    def get_context_data(self, **kwargs):

        context = {'foo':None,'baar':None}
        print context
        context['foo'] = 'peppo'


        context['alloggi'] = Alloggio.objects.all()




        return context







class AlloggioDetail(TemplateView):
    template_name = 'alloggio/detail.html'




    def get_context_data(self, **kwargs):
        context = {}

        if not kwargs.has_key('pk'):
            raise Http404

        context['alloggio'] = get_object_or_404(Alloggio, pk=kwargs['pk'])



        res = AlloggioResource()
        res.servizi_opzionali.full = True
        bundle = res.build_bundle(obj=context['alloggio'], request=self.request)
        # print bundle
        bundle = res.full_dehydrate(bundle, for_list=True)
        # print bundle

        context['alloggio_json'] = res.serialize(None, bundle, "application/json")




        res = GalleryResources()
        bundle = res.build_bundle(obj=context['alloggio'].gallery, request=self.request)
        # print bundle
        bundle = res.full_dehydrate(bundle, for_list=True)
        # print bundle

        context['gallery_json'] = res.serialize(None, bundle, "application/json")

        # pk = kwargs['pk']
        #
        # try:
        #     context['alloggio'] = Alloggio.objects.get(pk=pk)
        # except Alloggio.DoesNotExist:
        #     raise Http404

        return context





class AlloggioCreate(CreateView):
    template_name = 'alloggio/create.html'
    model = Alloggio
    form_class = AlloggioForm

    # success_url = '/alloggio/detail/%(id)s'

    def get_success_url(self):
        if self.success_url:
            return self.success_url % self.object.__dict__
        else:
            return reverse('alloggio_detail',kwargs={'pk':self.object.pk})


    def get(self, request, *args, **kwargs):
        if not self.request.user.isLocatore():
            return HttpResponseRedirect(reverse('registra_locatore'))

        return super(AlloggioCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AlloggioCreate,self).get_context_data(**kwargs)

        if not context.has_key('addressForm'):
            context['addressForm'] = FullAddressForm()

        return context


    def form_invalid(self, form,addressForm):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=form,addressForm=addressForm))


    def form_valid(self, form,address):
        """
        If the form is valid, save the associated model.
        """
        print 'form_valid',self.object
        self.object = form.save(commit=False)
        self.object.address = address
        self.object.owner = self.request.user
        self.object.save()



        recipients = getattr(settings,'',[])
        for r in recipients:
            send_mail('Nuovo alloggio', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)



        return super(AlloggioCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        print request.POST

        self.object = None



        addressForm = FullAddressForm(request.POST)
        # print addressForm
        if addressForm.is_valid():
            print 'addressForm isValid'
            address = addressForm.save()
        else:
            print 'addressForm invalid'
            address = None

        # self.context['addressForm'] = addressForm


        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            print 'form Valid'
            if not address:
                return self.form_invalid(form,addressForm)
            return self.form_valid(form,address)
        else:
            print 'form notValid'
            print form.errors
            return self.form_invalid(form,addressForm)


        # return super(AlloggioCreate,self).post(request,args,kwargs)





class AlloggioEdit(UpdateView):
    template_name = 'alloggio/create.html'
    model = Alloggio
    form_class = AlloggioForm

    def get_object(self, queryset=None):
        obj = super(AlloggioEdit,self).get_object(queryset)

        if not (self.request.user == obj.owner or self.request.user.is_staff):
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(AlloggioEdit,self).get_context_data(**kwargs)

        if not context.has_key('addressForm'):
            context['addressForm'] = FullAddressForm(instance=self.object.address)

        return  context


    def form_invalid(self, form,addressForm):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=form,addressForm=addressForm))


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        print request.POST
        addressForm = FullAddressForm(request.POST)
        if addressForm.is_valid():
            print 'addressForm isValid'
            address = addressForm.save()
        else:
            print 'addressForm invalid',addressForm
            address = None


        self.object.address = address
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form,addressForm)


class AlloggioSearch(TemplateView):
    template_name = 'alloggio/search.html'


    def post(self, request, *args, **kwargs):

        if not getattr(settings, 'SEIPETALI_SEARCH_ENABLED', True):
            return HttpResponseRedirect(urlresolvers.reverse('alloggio_search'))

        print 'POST: ',args,kwargs,request.POST

        searchForm = BaseSearchForm(request.POST)
        print searchForm.is_valid()



        return self.get(request, *args, **kwargs)



    # def get(self, request, *args, **kwargs):
    #     print args,kwargs
    #     print request.GET
    #
    #     return super(AlloggioSearch,self).get(args,kwargs)
    #
    # def get_context_data(self, **kwargs):
    #     print kwargs
    #     return {}




class AlloggioStartSearchView(TemplateView):
    template_name = 'alloggio/search_start.html'

    def post(self, request, *args, **kwargs):
        print 'POST: ',args,kwargs,request.POST

        searchForm = BaseSearchForm(request.POST)


        if searchForm.is_valid():
            # print 'SearchForm Valid',searchForm.cleaned_data
            url = urlresolvers.reverse('alloggio_search_map')
            url += '?checkin=%(checkin)s&checkout=%(checkout)s&numero_ospiti=%(numero_ospiti)s' % searchForm.cleaned_data
            return  HttpResponseRedirect(url)

        else:
            kwargs['searchForm'] = searchForm



        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AlloggioStartSearchView,self).get_context_data(**kwargs)

        if not kwargs.has_key('searchForm'):
            context['searchForm'] = BaseSearchForm(initial={'numero_ospiti':1})

        context['SEARCH_ENABLED'] = getattr(settings, 'SEIPETALI_SEARCH_ENABLED', True)

        return context




list = login_required(AlloggioList.as_view())
detail = login_required(AlloggioDetail.as_view())
create = login_required(AlloggioCreate.as_view())
edit = login_required(AlloggioEdit.as_view())
search_map  = AlloggioSearch.as_view()
search_start  = AlloggioStartSearchView.as_view()
