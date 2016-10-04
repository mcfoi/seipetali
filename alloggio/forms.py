__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, PrependedAppendedText,InlineCheckboxes,InlineField, PrependedText, Accordion ,AccordionGroup,Tab
from crispy_forms.layout import Submit, Layout, Field, Fieldset,Column,HTML,Button,Div,Reset
from modeltranslation.forms import TranslationModelForm,TranslationField

from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import DateInput
from common.widget import DateInputAngularBootstrapDatepicker
from django.utils.translation import ugettext_lazy as _

from django import forms
from models import Alloggio


class BaseSearchForm(forms.Form):
    helper = FormHelper()
    helper.form_tag = False
    helper.disable_csrf = True
    helper.form_method = 'POST'


    checkin = forms.DateField(required=True,widget=DateInputAngularBootstrapDatepicker)
    checkout = forms.DateField(required=True,widget=DateInputAngularBootstrapDatepicker)
    numero_ospiti = forms.IntegerField(required=True)


    def __init__(self, *args, **kw):
        super(BaseSearchForm, self).__init__(*args, **kw)
        self.fields['checkin'].widget.attrs['placeholder'] = _('Chek-in ')
        self.fields['checkout'].widget.attrs['placeholder'] = _('Chek-out ')
        self.fields['numero_ospiti'].widget.attrs['placeholder'] = _('Numero di ospiti ')




class AlloggioForm(TranslationModelForm):


    helper = FormHelper()
    helper.form_tag = False
    helper.disable_csrf = True
    helper.form_method = 'POST'


    helperTop = FormHelper()
    helperTop.form_tag = False
    helperTop.disable_csrf = True
    helperTop.form_method = 'POST'

    helperTop.layout = Layout(
         Div(
                Field('descrizione_breve', css_class='input-lg', wrapper_class='col-md-12'),
                Field('descrizione_lunga', css_class='input-lg', wrapper_class='col-md-12'),
                Field('regole_casa', css_class='input-lg', wrapper_class='col-md-12'),
                css_class='row'
            ),
         Div(
            Field('tipo', css_class='input-lg',wrapper_class='col-md-6'),
            Field('piano', css_class='input-lg', wrapper_class='col-md-4'),
            # Field('ascensore', css_class='input-lg', wrapper_class='col-md-2'),
            Div(
                        InlineField('ascensore'),
                        InlineField('accesso_disabili'),
                        InlineField('animali_ammessi'),
                        css_class='col-md-2'
                    ),
            Field('postiletto', css_class='input-lg', wrapper_class='col-md-3'),
            Field('descrizione_letti', css_class='input-lg',wrapper_class='col-md-9'),
                        css_class='row'
            ),

    )


    helper.layout = Layout(

        # Fieldset('Descrizione e regole',
        #     Div(
        #         Field('descrizione_breve', css_class='input-lg', wrapper_class='col-md-12'),
        #         Field('descrizione_lunga', css_class='input-lg', wrapper_class='col-md-12'),
        #         Field('regole_casa', css_class='input-lg', wrapper_class='col-md-12'),
        #         css_class='row'
        #     ),
        #     css_class='col-md-12'
        #  ),
        #
        #
        # Fieldset('Lavoro',
        #
        #          Div(
        # Field('tipo', css_class='input-lg',wrapper_class='col-md-6'),
        # Field('piano', css_class='input-lg', wrapper_class='col-md-4'),
        # Field('postiletto', css_class='input-lg', wrapper_class='col-md-6'),
        # Field('descrizione_letti', css_class='input-lg',wrapper_class='col-md-12'),
        #             css_class='row'
        #         ),
        #          css_class='col-md-12'
        # ),


        Fieldset('Varie',

                 Div(
                    Field('prezzo', css_class='input-lg', wrapper_class='col-md-3'),
                    Field('prezzo_week', css_class='input-lg', wrapper_class='col-md-3'),
                    Field('iva', css_class='input-lg', wrapper_class='col-md-3'),
                    # Div(
                    #     'ascensore',
                    #     'accesso_disabili',
                    #     'animali_ammessi',
                    #     # 'ascensore',
                    #     css_class='col-md-4'
                    # ),

                    # Field('ascensore', css_class='input-lg', wrapper_class='col-md-4'),
                    # Field('accesso_disabili', css_class='input-lg', wrapper_class='col-md-4'),
                    # Field('animali_ammessi', css_class='input-lg', wrapper_class='col-md-4'),
                    Field('posti_auto', css_class='input-lg', wrapper_class='col-md-3'),
                    Div(
                        InlineCheckboxes('servizi_base'),
                        css_class='col-md-4'
                    ),
                    # Div(
                    #     InlineCheckboxes('servizi_opzionali'),
                    #     css_class='col-md-4'
                    # ),
                    css_class='row'
                ),
                 css_class='col-md-12'
        ),


        # piano = models.IntegerField(default=0)
        # ascensore = models.BooleanField(default=False)
        # accesso_disabili = models.BooleanField(default=False)
        # animali_ammessi = models.BooleanField(default=False)
        # posti_auto = models.IntegerField(default=0)



        #
        # Div(
        #     InlineCheckboxes('teach_level',wrapper_class='col-md-12'),
        #     css_class='col-md-12'
        # ),
        #
        # # PrependedAppendedText('price', '$', '.00' ),
        # HTML('<div class="col-md-12" id="tagManager"></div>'),
        # HTML('<div class="col-md-12" ><hr></div>'),


    )


    class Meta:
        from django.forms import TextInput,Textarea
        model = Alloggio
        exclude = ('owner','address','calendar','letti')

        widgets = {
            'descrizione_breve': TextInput(),
            'descrizione_lunga': Textarea(attrs={'cols': 80, 'rows': 5,'style':"resize:none"}),
            'regole_casa': Textarea(attrs={'cols': 80, 'rows': 3,'style':"resize:none"}),
        }

        # widgets = {
        #     'servizi_base':  forms.ModelMultipleChoiceField()
        # }

    def __init__(self, *args, **kw):
        # initial=
        super(AlloggioForm, self).__init__(*args, **kw)

        for f in self._meta.model._meta.fields:
            print f,isinstance(f, TranslationField)
            # if f.name in self.fields and isinstance(f, TranslationField):
            #     del self.fields[f.name]
        # CHOICHE = ((1,'we'),(2,'23'))
        # print self.fields['servizi_base']
        # self.fields['servizi_base'].widget = forms.CheckboxSelectMultiple()