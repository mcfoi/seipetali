__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


from django.contrib import admin
from .models import User




admin.site.register(User)