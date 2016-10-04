
__author__ = 'elfo'


from modeltranslation.translator import translator, TranslationOptions
from models import Faq


class FaqTranslationOptions(TranslationOptions):
    fields = ('domanda', 'risposta',)

translator.register(Faq, FaqTranslationOptions)
