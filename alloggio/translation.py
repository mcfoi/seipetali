
__author__ = 'elfo'



from modeltranslation.translator import translator, TranslationOptions
from models import Alloggio,AbstractServizio,ServizioOpzionale,ServizioBase,Letto

class AlloggioTranslationOptions(TranslationOptions):
    fields = ('descrizione_breve', 'descrizione_lunga','regole_casa','descrizione_letti',)



class AbstractServizioTranslationOptions(TranslationOptions):
    fields = ('nome', 'descrizione',)


class LettoTranslationOptions(TranslationOptions):
    fields = ('descrizione',)



translator.register(Alloggio, AlloggioTranslationOptions)
translator.register(ServizioOpzionale, AbstractServizioTranslationOptions)
translator.register(ServizioBase, AbstractServizioTranslationOptions)
translator.register(Letto, LettoTranslationOptions)

