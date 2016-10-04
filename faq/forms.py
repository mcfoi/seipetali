__author__ = 'luca.affini'

from modeltranslation.forms import TranslationModelForm
from .models import Faq

# ============================================================================ #


class FaqForm (TranslationModelForm):
    # ============================================================================ #

    class Meta:
        model = Faq
