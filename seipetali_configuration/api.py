__author__ = 'elfo'

# import the logging library
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


from models import *
from common.api import BaseResource



class IvaResources(BaseResource):


    class Meta(BaseResource.Meta):
        queryset = Iva.objects.all()




