__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.contrib import admin
from django.contrib.sessions.models import Session




admin.site.register(Session)