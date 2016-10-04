__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


from cms.middleware.toolbar import ToolbarMiddleware
from django.core.urlresolvers import resolve


class CustomToolbarMiddleware(ToolbarMiddleware):

    def isCMS(self,request):

        try:
            match = resolve(request.path)
        except:
            return False

        if match.app_name == 'cms' or (match.app_name == 'admin' and 'cms' in match.url_name) :
            return True
        return False


    def process_request(self, request):
        if self.isCMS(request):
            super(CustomToolbarMiddleware,self).process_request(request)
        # else:
        #     return request


    def process_view(self, request, view_func, view_args, view_kwarg):
        if self.isCMS(request):
            return super(CustomToolbarMiddleware,self).process_view(request,view_func, view_args, view_kwarg)
        else:
            return

    def process_response(self, request, response):
        if self.isCMS(request):
            return super(CustomToolbarMiddleware,self).process_response(request,response)
        else:
            return response