__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django import template


register = template.Library()

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(name='min_times')
def min_times(number,min_val=None):
    if min_val:
        number = min(number,min_val)
    return range(number)