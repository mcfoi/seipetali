__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


from django.contrib import admin
from .models import Alloggio,ServizioBase,ServizioOpzionale,Letto,LettoRelation




admin.site.register(Alloggio)
admin.site.register(ServizioBase)
admin.site.register(ServizioOpzionale)
admin.site.register(Letto)
admin.site.register(LettoRelation)