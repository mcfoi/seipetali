from django import forms
from widgets import *


class ForeignKeyField(forms.ModelChoiceField):

    def __init__(self, queryset, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = ForeignKeySelect(queryset.model)
        return super(ForeignKeyField, self).__init__(queryset, *args, **kwargs)

    def _get_queryset(self):
        return self.queryset.model.all()


## A base form used for view deferral.
#
#  To defer a view with a form, the called view's forms must store the
#  deferred view's token.
#
class Callable(object):
    token = forms.CharField(required=False, widget=forms.HiddenInput())
