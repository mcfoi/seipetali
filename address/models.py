import urllib2
from django.db import models
from django.core.exceptions import ValidationError
from djangoutils.conv import to_address
# from googlemaps import GoogleMapsError
import datetime


import logging
logger = logging.getLogger(__name__)


__all__ = ['Country', 'State', 'Locality', 'Address', 'AddressField',
           'get_or_create_address']


class Country(models.Model):
    name = models.CharField(max_length=40, unique=True, blank=True)
    code = models.CharField(max_length=2, blank=True) # not unique as there are duplicates (IT)

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s'%(self.name or self.code  )


class State(models.Model):
    name = models.CharField(max_length=165, blank=True)
    code = models.CharField(max_length=3, blank=True, null=True)
    country = models.ForeignKey(Country, related_name='states')

    class Meta:
        unique_together = ('name', 'country')
        ordering = ('country', 'name')

    def __unicode__(self):
        txt = u'%s'%(self.name or self.code )
        country = u'%s'%self.country
        if country and txt:
            txt += u', '
        txt += country
        return txt


class Locality(models.Model):
    name = models.CharField(max_length=165, blank=True)
    postal_code = models.CharField(max_length=10, blank=True,null=True)
    state = models.ForeignKey(State, related_name='localities')

    class Meta:
        verbose_name_plural = 'Localities'
        unique_together = ('name', 'state','postal_code')
        ordering = ('state', 'name')

    def __unicode__(self):
        txt = u'%s'%self.name
        state = u'%s'%self.state
        code = u'%s'%self.postal_code
        if txt and code:
            txt += u', '
        txt += code

        if txt and state:
            txt += u', '
        txt += state
        return txt


class Address(models.Model):
    street_address = models.CharField(max_length=100, blank=True, null=True)
    street_number = models.CharField(max_length=6, blank=True, null=True)
    locality = models.ForeignKey(Locality, related_name='addresses', blank=True, null=True)
    formatted = models.CharField(max_length=200, blank=True, null=True)
    unformatted = models.CharField(max_length=200, blank=False)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Addresses'
        ordering = ('locality', 'street_address')


    def __unicode__(self):
        if self.formatted:
            return self.formatted
        else:
            txt = u'%s %s' % (self.street_address,self.street_number)
            locality = u'%s'%self.locality
            if txt and locality:
                txt += u', '
            txt += locality
            return txt

    def as_dict(self):
        return dict(
            street_address=self.street_address,
            street_number=self.street_number,
            locality=self.locality.name,
            postal_code=self.locality.postal_code,
            state=self.locality.state.name,
            state_code=self.locality.state.code,
            country=self.locality.state.country.name,
            country_code=self.locality.state.country.code,
            formatted=self.formatted,
            unformatted=self.unformatted,
            latitude=self.latitude,
            longitude=self.longitude,
        )

    @property
    def coordinate(self):
        return self.latitude, self.longitude


class AddressField(models.ForeignKey):
    __metaclass__ = models.SubfieldBase
    description = 'An address'

    def __init__(self, **kwargs):
        # print 'AddressField init ',kwargs
        kwargs.pop('to', None)
        self._geo_accuracy = kwargs.pop('geo_accuracy', 1)
        super(AddressField, self).__init__(Address, **kwargs)

    def str_to_dict(self, value):
        if value is None:
            return None

        # Check for a string not conforming to the serialised format.
        if isinstance(value, basestring):
            # TODO: Check for serialised version.
            # Convert to a tuple for the next part.
            value = (value,)

        # Check if we have a tuple first, because we will convert it to a dictionary
        # and let the dictionary handler deal with it.
        if isinstance(value, tuple) and len(value) >= 1:

            # Extract our name and address.
            if len(value) >= 2:
                name = value[0]
                address = value[1]
            else:
                name = None
                address = value[0]

            # Convert to a dictionary value.
            if name:
                try:
                    value = to_address(name + ' near ' + address, self._geo_accuracy)
                except  urllib2.HTTPError:
                    name = None
                except Exception as e:
                    name = None
            if not name:
                value = to_address(address, self._geo_accuracy)

        return value

    def to_python(self, value):
        print 'models.AddressField to_python', value
        try:
            value = self.str_to_dict(value)
        except urllib2.URLError as e:
            print 'No connection available'
            print e

        print value

        if value is None:
            return None

        # Is it already an address object?
        if isinstance(value, Address):
            return value

        # If we have an integer, assume it is a model primary key. This is mostly for
        # Django being a cunt.
        elif isinstance(value, (int, long)):
            return value

        # A dictionary of named address components.
        elif isinstance(value, dict):
            country = value.get('country', '')
            country_code = value.get('country_code', '')
            state = value.get('state', '')
            state_code = value.get('state_code', '')
            locality = value.get('locality', '')
            postal_code = value.get('postal_code', '')
            street_address = value.get('street_address', '')
            street_number = value.get('street_number', '')
            formatted = value.get('formatted', '')
            unformatted = value.get('unformatted', '')
            latitude = value.get('latitude', None)
            longitude = value.get('longitude', None)

            # Handle the country.
            country_obj, created = Country.objects.get_or_create(name=country)
            if created: print 'Created:',country_obj

            # try:
            #     country_obj = Country.objects.get(name=country)
            # except Country.DoesNotExist:
            #     country_obj = Country(name=country, code=country_code)

            # Handle the state.
            state_obj, created = State.objects.get_or_create(name=state, code=state_code, country=country_obj)
            if created: print 'Created:',state_obj

            # try:
            #     state_obj = State.objects.get(name=state, country=country_obj)
            # except State.DoesNotExist:
            #     state_obj = State(name=state, code=state_code, country=country_obj)

            # Handle the locality.
            locality_obj,created = Locality.objects.get_or_create(name=locality, postal_code=postal_code, state=state_obj)
            if created: print 'Created:',locality_obj
            # try:
            #     locality_obj = Locality.objects.get(name=locality, state=state_obj)
            # except Locality.DoesNotExist:
            #     locality_obj = Locality(name=locality, postal_code=postal_code, state=state_obj)


            address_obj,created = Address.objects.get_or_create(
                    street_address=street_address,
                    street_number=street_number,
                    locality=locality_obj,
                    formatted=formatted,
                    unformatted=unformatted,
                    latitude=latitude,
                    longitude=longitude,
                )
            # Handle the address.
            # try:
            #     address_obj = Address.objects.get(
            #         street_address=street_address,
            #         street_number=street_number,
            #         locality=locality_obj,
            #         formatted=formatted,
            #         unformatted=unformatted,
            #         latitude=latitude,
            #         longitude=longitude,
            #     )
            # except Address.DoesNotExist:
            #     address_obj = Address(
            #         street_address=street_address,
            #         street_number=street_number,
            #         locality=locality_obj,
            #         formatted=formatted,
            #         unformatted=unformatted,
            #         latitude=latitude,
            #         longitude=longitude,
            #     )

            # Need to save here to help Django on it's way.
            self._do_save(address_obj)

            # If "formatted" is empty try to construct it from other values.
            if not address_obj.formatted:
                address_obj.formatted = unicode(address_obj)
                address_obj.save()

            # Done.
            return address_obj

        # Try to deserialise a string ... how?
        raise ValidationError('Invalid locality value')

    def pre_save(self, model_instance, add):
        address = getattr(model_instance, self.name)
        return self._do_save(address)

    def formfield(self, **kwargs):
        from forms import AddressField as AddressFormField
        defaults = dict(form_class=AddressFormField)
        defaults.update(kwargs)
        return super(models.ForeignKey, self).formfield(**defaults)

    def value_from_object(self, obj):
        value = getattr(obj, self.name)
        return value

    def _do_save(self, address):
        if address is None:
            return address
        address.locality.state.country.save()
        address.locality.state.country_id = address.locality.state.country.pk
        address.locality.state.save()
        address.locality.state_id = address.locality.state.pk
        address.locality.save()
        address.locality_id = address.locality.pk
        address.save()
        return address.pk

    def get_prep_value(self,value):
        print 'in get prep value',datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%f")
        return value.id

    def get_db_prep_value(self,value,connection,prepared=False):
        print 'in get Db prep value',datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M:%f")
        return value.id

# def do_save(address):
#     if address is None:
#         return address
#     address.locality.state.country.save()
#     address.locality.state.country_id = address.locality.state.country.pk
#     address.locality.state.save()
#     address.locality.state_id = address.locality.state.pk
#     address.locality.save()
#     address.locality_id = address.locality.pk
#     address.save()
#     return address.pk
#
#
# def get_or_create_address(value, geo_accuracy=1):
#     def str_to_dict(value):
#         if value is None:
#             return None
#
#         # Check for a string not conforming to the serialised format.
#         if isinstance(value, basestring):
#             # TODO: Check for serialised version.
#             # Convert to a tuple for the next part.
#             value = (value,)
#
#         # Check if we have a tuple first, because we will convert it to a dictionary
#         # and let the dictionary handler deal with it.
#         if isinstance(value, tuple) and len(value) >= 1:
#
#             # Extract our name and address.
#             if len(value) >= 2:
#                 name = value[0]
#                 address = value[1]
#             else:
#                 name = None
#                 address = value[0]
#
#             # Convert to a dictionary value.
#             if name:
#                 try:
#                     value = to_address(name + ' near ' + address, geo_accuracy)
#                 except GoogleMapsError, urllib2.HTTPError:
#                     name = None
#             if not name:
#                 value = to_address(address, geo_accuracy)
#
#         return value
#
#     def to_python(value):
#         value = str_to_dict(value)
#         if value is None:
#             return None
#
#         # Is it already an address object?
#         if isinstance(value, Address):
#             return value
#
#         # If we have an integer, assume it is a model primary key. This is mostly for
#         # Django being a cunt.
#         elif isinstance(value, (int, long)):
#             return value
#
#         # A dictionary of named address components.
#         elif isinstance(value, dict):
#             country = value.get('country', '')
#             country_code = value.get('country_code', '')
#             state = value.get('state', '')
#             state_code = value.get('state_code', '')
#             locality = value.get('locality', '')
#             postal_code = value.get('postal_code', '')
#             street_number = value.get('street_number', '')
#             street_address = value.get('street_address', '')
#             formatted = value.get('formatted', '')
#             latitude = value.get('latitude', '')
#             longitude = value.get('longitude', '')
#
#             # If there is nothing here then just return None.
#             if not (country or country_code or state or state_code or
#                     locality or postal_code or street_address or street_number or
#                     latitude or longitude):
#                 return None
#
#             # Handle the country.
#             try:
#                 country_obj = Country.objects.get(name=country)
#             except Country.DoesNotExist:
#                 country_obj = Country(name=country, code=country_code)
#
#             # Handle the state.
#             try:
#                 state_obj = State.objects.get(name=state, country=country_obj)
#             except State.DoesNotExist:
#                 state_obj = State(name=state, code=state_code, country=country_obj)
#
#             # Handle the locality.
#             try:
#                 locality_obj = Locality.objects.get(name=locality, state=state_obj)
#             except Locality.DoesNotExist:
#                 locality_obj = Locality(name=locality, postal_code=postal_code, state=state_obj)
#
#             # Handle the address.
#             try:
#                 address_obj = Address.objects.get(
#                     street_address=street_address,
#                     street_number=street_number,
#                     locality=locality_obj,
#                     formatted=formatted,
#                     latitude=latitude,
#                     longitude=longitude,
#                 )
#             except Address.DoesNotExist:
#                 address_obj = Address(
#                     street_address=street_address,
#                     street_number=street_number,
#                     locality=locality_obj,
#                     formatted=formatted,
#                     latitude=latitude,
#                     longitude=longitude,
#                 )
#
#             # Need to save here to help Django on it's way.
#             do_save(address_obj)
#
#             # If "formatted" is empty try to construct it from other values.
#             if not address_obj.formatted:
#                 address_obj.formatted = unicode(address_obj)
#                 address_obj.save()
#
#             # Done.
#             return address_obj
#
#         # Try to deserialise a string ... how?
#         raise ValidationError('Invalid locality value')
#
#     return to_python(value)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^address\.models\.AddressField'])
except:
    pass
