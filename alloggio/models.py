__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from  datetime import datetime
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q,F
from django.template.defaultfilters import slugify

from schedule.models import Calendar,Event
import dateutil.parser
from datetime import date, timedelta
from decimal import Decimal as D
from seipetali_configuration.models import Iva
import string
from django.db import transaction
# from django.core.mail import get_connection, EmailMultiAlternatives
# from django.template.loader import render_to_string
from notification.models import NoticeType
from notification.backends import  email as notification_email

@property
def get_alloggio(self):
    return self.alloggio_set.first()

Calendar.add_to_class('alloggio', get_alloggio)



def calcIva(n,iva=None):
    if not isinstance(n, D):
        n = D(n)

    if not iva:
        try:
            iva_perc = Iva.objects.filter(def_iva=True).first().val_perc
        except:
            iva_perc = 22
    else:
        iva_perc = iva.val_perc

    return D(n)*D(iva_perc)/D(100)



# SERVIZI CONNESSI AGLI ALLOGGI
class AbstractServizio(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    nome = models.CharField(null=False,max_length=64)
    descrizione = models.CharField(null=False,max_length=500)

    def __unicode__(self):
        return u"%s " % (self.nome)

    class Meta:
        abstract = True




class ServizioBase(AbstractServizio):
    class Meta:
        verbose_name = "servizio base"



class ServizioOpzionale(AbstractServizio):

    costo = models.DecimalField(max_digits=12, decimal_places=2,null=False,blank=False)
    fattore_tempo = models.IntegerField(null=False,default=1)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,null=False,blank=False)
    iva = models.ForeignKey('seipetali_configuration.Iva',null=True)


    class Meta:
        verbose_name = "servizio Opzionale"



    def getServicePrice(self,notti=None,ospiti=None):
        if not notti:
            raise Exception('Numero notti obbligatorio')

        prezzo =  D(notti * self.costo)
        iva = calcIva(prezzo,self.iva)
        totale = prezzo+iva

        return { 'type':self.__class__.__name__ ,
                 'id':self.id ,
                 'prezzo' :prezzo ,
                 'iva' :iva ,
                 'totale' :totale ,
                 }




# LETTI

class Letto(models.Model):
    postiletto = models.PositiveIntegerField(null=False,blank=False)
    descrizione = models.CharField(null=False,max_length=64)


    def __unicode__(self):
        return u"%s (%d postiletto)" % (self.descrizione,self.postiletto    )




# ALLOGGIO

class AlloggioManager(models.Manager):

    def filter_free_for_date(self, start, end):



        if isinstance(start,str) or isinstance(start,unicode):
            start = dateutil.parser.parse(start)

        if isinstance(end,str) or isinstance(end,unicode):
            end = dateutil.parser.parse(end)

        # print type(start),type(end)

        start = start + timedelta(minutes=1)
        # end = end - timedelta(minutes=10)

        # print 'AlloggioManager  filter_free_for_date ',start,end

        # ct = ContentType.objects.get_for_model(type(self))
        # if distinction:
        #     dist_q = Q(calendarrelation__distinction=distinction)
        # else:
        #     dist_q = Q()
        # print self.get_queryset()

        # return self.filter( Q(calendarrelation__object_id=obj.id, calendarrelation__content_type=ct))
        # queryset = Calendar.objects.exclude(
        #     Q(
        #         event__start__gt=start,
        #         event__start__lt=end
        #     ) |
        #     Q(
        #         event__end__gt=start,
        #         event__end__lt=end
        #     )
        # )
        #
        # print queryset
        #
        # # queryset = Calendar.objects.exclude(
        # #     event__start__gte=F(start),
        # #     event__end__lte=F(end)
        # # )
        #
        #
        # print queryset
        # print 'filter_free_for_date',start,end
        # print  self.get_queryset()

        # queryset = self.get_queryset().exclude(
        #     Q(
        #         calendar__event__start__gt=start,
        #         calendar__event__start__lt=end
        #     ) |
        #     Q(
        #         calendar__event__end__gt=start,
        #         calendar__event__end__lt=end
        #     ))


        # queryset = self.get_queryset().exclude(
        #     Q(
        #         Q(calendar__event__start__gt=start),
        #         Q(calendar__event__start__lt=end)
        #     ) |
        #     Q(
        #         Q(calendar__event__end__gt=start),
        #         Q(calendar__event__end__lt=end)
        #     ))

        queryset = self.get_queryset().exclude(
                Q(calendar__event__start__range=(start,end))
                |
                Q(calendar__event__end__range=(start,end))
            )
        # queryset = self.get_queryset().exclude(Q(calendar__event__start__gt=start),Q(calendar__event__start__lt=end))

        # print queryset.query
        # print queryset


        return queryset

class Alloggio(models.Model):


    ALLOGGIO_APPARTAMENTO = 'appartamento'
    ALLOGGIO_CASA_SINGOLA = 'singola'
    ALLOGGIO_RESIDENCE = 'residence'

    ALLOGGIO_TYPE = (
        (ALLOGGIO_APPARTAMENTO,'Appartamento'),
        (ALLOGGIO_CASA_SINGOLA,'Casa Singola'),
        (ALLOGGIO_RESIDENCE,'Residence'),
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,null=False,blank=False)


    active = models.BooleanField(null=False,default=False)

    tipo = models.CharField(null=False,max_length=16,choices=ALLOGGIO_TYPE,default=ALLOGGIO_APPARTAMENTO)
    descrizione_breve = models.TextField(verbose_name="Descrizione alloggio",null=False,max_length=100)
    descrizione_lunga = models.TextField(verbose_name="Descrizione dettagliata",null=False,max_length=1000)
    regole_casa = models.TextField(verbose_name="Regole della casa e informazioni varie",null=False,max_length=1000)


    postiletto = models.PositiveIntegerField(null=False,blank=False)
    descrizione_letti = models.CharField(null=False,max_length=100)

    # Questa parte serve a popolare la whishlist degli utenti e la registrazione prodotto:
    # si accede dall'utente tarmite   letto.whishlist_product.all() e user.registered_product.all()
    letti = models.ManyToManyField(Letto, through='LettoRelation',null=True,blank=True)


    prezzo = models.FloatField(null=False,default=0.0)
    prezzo_week = models.FloatField(null=False,default=0.0)
    iva = models.ForeignKey('seipetali_configuration.Iva',null=True,blank=True)


    servizi_base = models.ManyToManyField('ServizioBase',null=True,blank=True)
    servizi_opzionali = models.ManyToManyField('ServizioOpzionale',null=True,blank=True)


    piano = models.IntegerField(default=0)
    ascensore = models.BooleanField(default=False)
    accesso_disabili = models.BooleanField(default=False)
    animali_ammessi = models.BooleanField(default=False)
    posti_auto = models.IntegerField(default=0)


    gallery = models.ForeignKey('photologue.Gallery')
    address = models.ForeignKey('address.Address')
    calendar = models.ForeignKey('schedule.Calendar',null=False,blank=True)



    objects = AlloggioManager()

    def __unicode__(self):
        return u"%s posti:%s of %s " % (self.tipo,self.postiletto,self.owner)

    def get_absolute_url(self):
        return reverse('alloggio_detail', kwargs={'pk':self.pk})


    def save(self, *args, **kwargs):

        if not self.calendar_id:
            if self.pk:
                self.calendar = Calendar.objects.get_or_create_calendar_for_object(self)
            else:
                name = u'Calendar '+datetime.now().strftime("%Y%m%d-%H%M%S")
                calendar = Calendar(name=name)
                calendar.slug = slugify(calendar.name)
                calendar.save()
                self.calendar = calendar
                obj = super(Alloggio, self).save(*args, **kwargs)
                calendar.create_relation(self)
                return obj

        return super(Alloggio, self).save(*args, **kwargs)


    # @property
    # def calendar(self):
    #     return Calendar.objects.get_or_create_calendar_for_object(self)

    @property
    def events(self):
        return self.calendar.events.all()



    def getAlloggioPrice(self,notti=None,ospiti=None):
        if not notti:
            raise Exception('Numero notti obbligatorio')

        if self.prezzo_week and not (notti % 7):
            prezzo =  D((notti/7) * self.prezzo_week)
        else:
            prezzo =  D(notti * self.prezzo)



        iva = calcIva(prezzo,self.iva)
        totale = prezzo+iva

        return { 'type':self.__class__.__name__ ,
                 'id':self.id ,
                 'prezzo' :prezzo ,
                 'iva' :iva ,
                 'totale' :totale ,
                 }

    @transaction.atomic
    def book(self,start=None,end=None,numero_ospiti=None,servizi_opzionali=[],user=None,session=None):
        print 'Alloggio book'
        print 'user:',user
        print 'session:',session

        day_count = end-start
        notti = day_count.days

        reservation = Reservation()
        if user.is_authenticated():
            reservation.user = user

        # if not session.exists(session.session_key):
        #     session.create()
        #
        # reservation.session = Session.objects.get(session_key=session.session_key)
        reservation.alloggio = self
        reservation.numero_ospiti = numero_ospiti


        alloggio_quote = self.getAlloggioPrice(notti,numero_ospiti)
        reservation.price = alloggio_quote['prezzo']
        reservation.iva = alloggio_quote['iva']



        reservation_event = Event(start=start,end=end,calendar=self.calendar,title='reservation ')

        reservation_event.save()
        reservation.event = reservation_event

        reservation.save()
        if user.is_authenticated():
            reservation.notify_reservation()




        for service in servizi_opzionali:
            reservation_service = ReservationService(original_service=service,reservation=reservation)
            reservation_quote = service.getServicePrice(notti,numero_ospiti)
            reservation_service.costo = service.costo
            reservation_service.fattore_tempo = service.fattore_tempo
            reservation_service.price = reservation_quote['prezzo']
            reservation_service.iva = reservation_quote['iva']
            reservation_service.save()

            # reservation.servizi_opzional.add(reservation_service)

        # reservation.servizi_opzional = servizi_opzionali

        return reservation




    def getQuote(self,start=None,end=None,numero_ospiti=None,servizi_opzionali=[]):
        # print 'Alloggio getQuote',start,end,numero_ospiti,servizi_opzionali

        if not start or not end or end < start:
            raise Exception('Quote non available! Check Date')



        day_count = end-start
        notti = day_count.days

        # Controlla che siano prenotazioni settimanali
        if day_count.days % 7 != 0:

            next = end+timedelta(days=(7-(day_count.days % 7)))
            availables = [next]


            # msg = 'Sono possibili solo prenotazioni settimanali!\nProva a prenotare fino al %s' % next.strftime('%d, %b %Y')

            if day_count.days > 7:
                prev = end-timedelta(days=(day_count.days % 7))
                # msg = msg + ' o al %s' % prev.strftime('%d, %b %Y')
                availables.insert(0,prev)

            str_availables = [d.strftime('%d %b %Y') for d in availables]
            msg = 'Sono possibili solo prenotazioni settimanali!\nProva a prenotare fino al %s' % string.join(str_availables,' o al ')
            raise Exception(msg)



        quote_detail = []
        quote_detail.append(self.getAlloggioPrice(notti,numero_ospiti))



        for service in servizi_opzionali:
            quote_detail.append(service.getServicePrice(notti,numero_ospiti))


        total = sum([i['totale'] for i in quote_detail])

        caparra = D(total * D(0.20)).quantize(D('1'))




        quote = {}
        quote['detail'] = quote_detail
        quote['total'] = total
        quote['caparra'] = caparra

        return quote

    def notify_on_create(self):
        recipients = getattr(settings, 'SEIPETALI_ADMINS', [])
        recipients = [i[1] for i in recipients]

        try:
            notice_type = NoticeType.objects.get(label="new_alloggio")
        except NoticeType.DoesNotExist:
            notice_type = NoticeType().create(label="new_alloggio", display='Notifica creazione alloggio', description='Notifica creazione alloggio')

        #recipients = recipients[:1]
        # print recipients, notice_type, notice_type.id
        # if True:
        #     return


        for mail in recipients:
            try:
                notification_email.EmailBackend(10).deliver_to_recipient_email(mail, None, notice_type,  {"alloggio": self })
            except:
                pass

        # html_content = render_to_string('newsletter.html', {'newsletter': n,})
        # text_content = "..."
        # msg = EmailMultiAlternatives("subject", text_content, "from@bla", ["to@bla", "to2@bla", "to3@bla"], connection=connection)
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()


# RELATION CLASS


class LettoRelation(models.Model):
    letto = models.ForeignKey(Letto)
    alloggio = models.ForeignKey(Alloggio)
    count = models.PositiveIntegerField(null=False,blank=False,default=1)
    note = models.TextField(null=False,max_length=100)


from reservation.models import Reservation,ReservationService



def alloggio_post_save(sender, instance, created, **kwargs):
    if created:
        instance.notify_on_create()

models.signals.post_save.connect(alloggio_post_save, sender=Alloggio)
