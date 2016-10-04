__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



from django.db import models
from django.conf import settings





class Parametri(models.Model):
    tariffa_mediazione_perc = models.FloatField(null=False,default=5)
    tariffa_gestione_perc = models.FloatField(null=False,default=2)






class Iva(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    nome = models.CharField(null=False,max_length=32)
    val_perc = models.FloatField(null=False)

    default = models.BooleanField(default=False)
    note = models.CharField(null=False,max_length=100)


    def __unicode__(self):
        return u"%s %% (%s)" % (self.val_perc,self.nome)



