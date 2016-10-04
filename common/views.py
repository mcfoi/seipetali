__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
from django.views.generic import TemplateView
import os


class StaticView(TemplateView):
    def get(self, request, page, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # print context

        pageName, extension = os.path.splitext(page)
        self.template_name = 'ng-template/' + pageName + '.html'
        return self.render_to_response(context)



reverse_staticView = StaticView.as_view()


