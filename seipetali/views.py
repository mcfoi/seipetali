__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from alloggio.forms import BaseSearchForm

from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from  django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core import urlresolvers
from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse

from cms.templatetags.cms_tags import PageUrl

from common.utils import get_cms_page_url

class HomeView(TemplateView):
    template_name = 'seipetali/home.html'



    def get(self, request, *args, **kwargs):
        homepage_visited = self.request.session.get('homepage_visited',False)


        if homepage_visited and not getattr(settings,'SHOW_HOME_ALWAYS',False):
            pageurl = get_cms_page_url('chi_siamo',self.request)
            return redirect(pageurl)
        else:
            self.request.session['homepage_visited'] = True
            return super(HomeView,self).get(request, *args, **kwargs)



class DashboardCallCenterView(TemplateView):
    template_name = 'seipetali/dashboards/callcenter.html'

    # def post(self, request, *args, **kwargs):
    #     print 'POST: ',args,kwargs,request.POST
    #
    #     searchForm = BaseSearchForm(request.POST)
    #
    #
    #     if searchForm.is_valid():
    #         # print 'SearchForm Valid',searchForm.cleaned_data
    #         url = urlresolvers.reverse('alloggio_search')
    #         url += '?checkin=%(checkin)s&checkout=%(checkout)s&numero_ospiti=%(numero_ospiti)s' % searchForm.cleaned_data
    #         return  HttpResponseRedirect(url)
    #
    #     else:
    #         kwargs['searchForm'] = searchForm
    #
    #
    #
    #     return self.get(request, *args, **kwargs)
    #
    # def get_context_data(self, **kwargs):
    #     context = super(DashboardCallCenterView,self).get_context_data(**kwargs)
    #
    #     return context


class SeipetaliCardView(TemplateView):
    template_name = 'seipetali/seipetalicard.html'





# from django.utils.functional import lazy
# reverse_lazy = lazy(reverse, unicode)


def is_staff_required(login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if user.is_staff:
            return True
        return False
    return user_passes_test(check_perms, login_url=login_url)


home = HomeView.as_view()
dashboard_call_center = is_staff_required(login_url='/')(DashboardCallCenterView.as_view())
seipetali_card = SeipetaliCardView.as_view()
