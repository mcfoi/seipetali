__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.contrib.auth.decorators import login_required


from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse

from .models import Faq
from .forms import FaqForm

# ============================================================================ #
class FaqList(TemplateView):
    # ============================================================================ #
    template_name = 'faq/list.html'

    def get_context_data(self, *args, **kwargs):

        context = {'gruppo': None, 'gruppi': None, 'faqs': None}
        print context
        print kwargs, args

        gruppo = False
        if kwargs.has_key('gruppo'):
            gruppo = kwargs['gruppo']

        if not gruppo:
            # context['gruppo'] = " - tutti"
            context['faqs'] = Faq.objects.all()
        else:
            context['gruppo'] = gruppo
            context['faqs'] = Faq.objects.filter(gruppo=gruppo)

        context['gruppi'] = Faq.FAQ_GRUPPI

        return context


# ============================================================================ #
class FaqCreate(CreateView):
    # ============================================================================ #
    template_name = 'faq/create.html'
    model = Faq
    form_class = FaqForm

    # success_url = '/faq/detail/%(id)s'

    # ------------------------ #
    def get_success_url(self):
        # ------------------------ #
        if self.success_url:
            return self.success_url % self.object.__dict__
        else:
            return reverse('faq_list')


# ============================================================================ #
class FaqEdit(UpdateView):
    # ============================================================================ #

    template_name = 'faq/create.html'
    model = Faq
    form_class = FaqForm

    # success_url = '/faq/detail/%(id)s'

    # ------------------------ #
    def get_success_url(self):
        # ------------------------ #

        if self.success_url:
            return self.success_url % self.object.__dict__
        else:
            return reverse('faq_list')


list = FaqList.as_view()
create = FaqCreate.as_view()
edit = FaqEdit.as_view()

