from django.db import models
from django.db.models import Q
from django.db.models.fields.related import RelatedField, ManyToManyField
from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404, _get_queryset
import conv

import logging
logger = logging.getLogger(__name__)


def model_fill(obj, info_dict):
    all_fields = obj._meta.fields + obj._meta.many_to_many
    for field in all_fields:
        if field.name in ['id', 'pk']:
            continue
        if field.name not in info_dict:
            continue
        name = field.name
        cur_val = getattr(obj, field.name)
        if isinstance(field, ManyToManyField):
            for val in conv.to_list(info_dict[field.name]):
                if not cur_val.filter(pk=val.pk).exists():
                    cur_val.add(val)
        else:
            if not cur_val:
                setattr(obj, field.name, info_dict[field.name])


def model_set_non_manytomany(obj, info_dict):
    all_fields = obj._meta.fields
    for field in all_fields:
        if field.name in ['id', 'pk']:
            continue
        if field.name not in info_dict:
            continue
        setattr(obj, field.name, info_dict[field.name])


def model_set_manytomany(obj, info_dict):
    all_fields = obj._meta.many_to_many
    for field in all_fields:
        if field.name in ['id', 'pk']:
            continue
        if field.name not in info_dict:
            continue
        setattr(obj, field.name, info_dict[field.name])


class FillModel(object):

    def fill(self, **kwargs):
        model_fill(self, kwargs)


## A model manager that uses a set of fields to identify records.
#
# On many occasions it is useful to be able to identify existing records based on a
# set of fields. This manager helps in this regard.
class UniqueManager(models.Manager):

    ## Initialise the manager.
    #
    # Accepts the fields to be used to uniquely identify records.
    #
    # @param[in]  id_fields  Keyword argument, a list of field names used to identify records.
    def __init__(self, *args, **kwargs):
        self._id_fields = kwargs.pop('id_fields', [])
        models.Manager.__init__(self, *args, **kwargs)

    ## Get an existing record.
    #
    # Takes a set of field values and attempts to find a unique record based on those values.
    # If not all required unique fields have been provided an exception will be raised. If no
    # such record can be found a standard Django exception will be raised.
    #
    # @param[in]  kwargs  Key/value pairs of fields and values.
    def get_existing(self, **kwargs):
        args = []
        for id_field in self._id_fields:
            if id_field not in kwargs or kwargs[id_field] is None:
                break
            args.append(Q(**{id_field: kwargs[id_field]}) | Q(**{id_field + '__isnull': True}))
        if not args:
            raise FieldError
        return models.Manager.get(self, *args)

    ## Get an existing record or create a new one.
    #
    # Takes a set of field values and attempts to find a unique record based on those values.
    # If not all required unique fields have been provided an exception will be raised. If no
    # such record can be found a new record will be created and returned.
    #
    # @param[in]  kwargs  Key/value pairs of fields and values.
    def get_existing_or_create(self, **kwargs):
        try:
            return self.get_existing(**kwargs), False
        except self.model.DoesNotExist:
            obj = self.model()
            model_set_non_manytomany(obj, kwargs)
            obj.save()
            model_set_manytomany(obj, kwargs)
            obj.save()
            return obj, True


def get_unique_fields(obj):
    return [f.name for f in obj._meta.fields if f.unique and f.name != 'id']


def get_unique_together_fields(obj):
    return obj._meta.unique_together


def get_duplicate(obj, qs=None):
    # Combine field names for the unique fields and those involved in any
    # 'unique_together' relationship.
    unique_together = [list(f) for f in get_unique_together_fields(obj)]
    unique_fields = set(get_unique_fields(obj) + sum(unique_together, []))

    # Construct a filter for each unique field.
    fltr = []
    for name in get_unique_fields(obj):
        val = getattr(obj, name)
        if val is None:
            fltr.append(Q(**{name + '__isnull': True}))
        else:
            fltr.append(Q(**{name: val}))

    # Construct a filter for each unique together field.
    for name_set in get_unique_together_fields(obj):
        group = []
        for name in name_set:
            val = getattr(obj, name)
            if val is None:
                group.append(Q(**{name + '__isnull': True}))
            else:
                group.append(Q(**{name: val}))
        if group:
            fltr.append(reduce(lambda x,y: x&y, group))

    # Reduce the filter using 'or' operators.
    if fltr:
        fltr = reduce(lambda x,y: x|y, fltr)

    # Get a queryset to check in.
    if qs is None:
        qs = obj.__class__.objects

    # If there is no filter there can be no duplicates, return an empty set.
    if not fltr:
        return qs.empty()
    else:
        return qs.get(fltr)


def follow(obj, attr, default=None):
    attrs = attr.split('__')
    for attr in attrs:
        if not hasattr(obj, attr):
            return default
        obj = getattr(obj, attr)
    return obj
