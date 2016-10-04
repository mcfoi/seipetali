__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
LOGGER = logging.getLogger(__name__)

from django.db import models


class Faq(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    domanda = models.TextField(null=False, max_length=500)
    risposta = models.TextField(null=False, max_length=1000)

    FAQ_GRUPPI = (
        ('info_locatore', 'Info locatore'),
        ('info_locatario', 'Info locatario'),
        ('categoria', 'Categoria'),
        ('altro', 'Altro'),
    )
    gruppo = models.CharField(
        max_length=30, choices=FAQ_GRUPPI, default='altro')

    def __unicode__(self):
        return u"%s " % (self.domanda)
