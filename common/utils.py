__author__ = 'elfo'
# -*- coding: utf-8 -*-

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



from cms.templatetags.cms_tags import PageUrl

def get_cms_page_url(pagename,request=None):
    if not request:
        raise Exception('no request found')

    context = {}
    context['request'] = request
            # func = PageUrl.__dict__['get_value']
    pageurl = PageUrl.__dict__['get_value'](PageUrl,context,pagename,None,None)
    return pageurl