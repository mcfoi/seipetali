__author__ = 'elfo'
# -*- coding: utf-8 -*-

# import the logging library
import logging
from .models import User
from django import forms
# Get an instance of a logger
logger = logging.getLogger(__name__)
from django.utils.translation import pgettext, ugettext_lazy as _, ugettext

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, PrependedAppendedText,InlineCheckboxes,InlineField, PrependedText, Accordion ,AccordionGroup,Tab
from crispy_forms.layout import Submit, Layout, Field, Fieldset,Column,HTML,Button,Div,Reset



class LocatoreForm(forms.ModelForm):
    terms = forms.BooleanField(
        label=_("Accetta i termini e le condizioni di servizio"),
        required=True,
        error_messages={'required':_("E' necessario accettare i termini e le condizioni di servizio")}
    )

    def __init__(self,terms_url=None, *args, **kw):
        if terms_url:
            self.terms_url = terms_url
        super(LocatoreForm, self).__init__(*args, **kw)
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs['placeholder'] = _("Nome")
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs['placeholder'] = _("Cognome")
        self.fields['phone_number'].required = True
        self.fields['phone_number'].widget.attrs['placeholder'] = _("+39 02 9876543")

        self.fields['address'].widget.attrs['placeholder'] = _(u"Indirizzo")
        self.fields['citta'].widget.attrs['placeholder'] = _(u"Cittá")
        self.fields['provincia'].widget.attrs['placeholder'] = _(u"Provincia")
        self.fields['postal_code'].widget.attrs['placeholder'] = _(u"Codice postale")

    class Meta:

        model = User
        fields = ('first_name','last_name','phone_number','address','citta','provincia','postal_code')

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        helper.form_method = 'POST'


        helper.layout = Layout(
             Div(
                    Field('first_name', css_class='input-lg', wrapper_class='col-md-12'),
                    Field('last_name', css_class='input-lg', wrapper_class='col-md-12'),
                    Field('phone_number', css_class='input-lg', wrapper_class='col-md-12'),
                    Field('address', css_class='input-lg', wrapper_class='col-md-12'),
                    Field('citta', css_class='input-lg', wrapper_class='col-md-4'),
                    Field('provincia', css_class='input-lg', wrapper_class='col-md-4'),
                    Field('postal_code', css_class='input-lg', wrapper_class='col-md-4'),
                    css_class='row'
                ),
             Div(
                    Field('terms', css_class='', wrapper_class='col-xs-6'),
                    HTML( '<div class="col-xs-6"> <a onclick="window.open(\'%s\',\'terms\',\'resizable,width=200\'); return false" href=""> Leggi le nostre condizioni </a> </div>' % self.terms_url),

                    css_class='row'
                ),

        )
        return helper
