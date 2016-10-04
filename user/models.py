# -*- coding: utf-8 -*-
__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



from django.db import models
from django.contrib.auth.models import UserManager,BaseUserManager,AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import factory
from django.utils.translation import ugettext_lazy as _
from faker import Factory as FakerFactory





class User(AbstractUser):

    phone_number = PhoneNumberField(null=True,blank=True)

    locatore = models.BooleanField(null=False, editable=False, default=False)
    locatario = models.BooleanField(null=False, editable=False, default=True)

    address = models.CharField(_(u'Indirizzo'), max_length=300, null=True, blank=True)
    citta = models.CharField(_(u'Cittá'), max_length=100, null=True, blank=True)
    provincia = models.CharField(_(u'Provincia'), max_length=100, null=True, blank=True)
    postal_code = models.CharField(_(u'Codice postale'), max_length=100, null=True, blank=True)

    def isLocatore(self):
        return self.locatore

    def isLocatario(self):
        return self.locatario





#####################
# User factory
faker = FakerFactory.create('it_IT')

class UserFactory(factory.Factory):
    # FACTORY_FOR = User

    class Meta:
        model = User
    #
    # title = factory.LazyAttribute(lambda x: faker.sentence(nb_words=4))
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    email = factory.LazyAttribute(lambda x: faker.email())
    username = factory.LazyAttribute(lambda x: faker.user_name())

    # firstname = "John"
    # lastname = "Doe"


