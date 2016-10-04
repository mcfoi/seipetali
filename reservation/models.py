__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.sessions.models import Session
from decimal import Decimal as D
from dataqrcode.models import DataQRCode
from django.contrib.sites.models import Site
import urllib
from django.core.mail import send_mail

from django.db.models import get_app
from notification.backends import  email as notification_email
from notification.models import NoticeType

class ReservationService(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    original_service = models.ForeignKey('alloggio.ServizioOpzionale',null=True,blank=True)
    reservation = models.ForeignKey('Reservation',related_name='servizi_opzional')

    costo = models.DecimalField(max_digits=12, decimal_places=2,null=False,blank=False)
    fattore_tempo = models.IntegerField(null=False,default=1)

    price = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                 blank=True)
    iva = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                 blank=True)


    def count(self):
        return self.reservation.getDayCount() / self.fattore_tempo



    def getTotal(self):
        return self.price+self.iva




class Reservation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=False)
    # session = models.ForeignKey(Session,null=True,blank=True,on_delete=models.SET_NULL)
    alloggio = models.ForeignKey('alloggio.Alloggio',null=False,blank=False)
    event = models.ForeignKey('schedule.Event')

    numero_ospiti = models.IntegerField(null=False,blank=False)
    # servizi_opzional = models.ManyToManyField('ReservationService',null=True,blank=True)
    qr_code = models.ForeignKey('dataqrcode.DataQRCode',blank=True,null=True,on_delete=models.SET_NULL)


    STATUS_PENDING = 'pending'
    STATUS_RESERVED = 'reserved'


    RESERVATION_STATUS = (
        (STATUS_PENDING,_('Pending')),
        (STATUS_RESERVED,_('Reserved')),
    )
    status = models.CharField(max_length=10,choices=RESERVATION_STATUS,default=STATUS_PENDING)




    price = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                 blank=True)
    iva = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                 blank=True)

    total = models.DecimalField(max_digits=12, decimal_places=2, null=True,
                                 blank=True)


    def qr_code_img(self):
        if self.qr_code :
            return self.qr_code.qr_code(css_class='img-rounded',size='100')
    qr_code_img.allow_tags = True

    def get_params_url(self):
        site = Site.objects.get_current()
        root_url = 'http://%s' % site.domain
        full_url = '%s%s' % ( root_url, self.get_absolute_url())
        params = {'pk':self.id , 'class':self.__class__.__name__}
        paramUri = '%s?%s' % (full_url, urllib.urlencode(params))
        return paramUri


    @models.permalink
    def get_absolute_url(self):
        return ('reservation_detail', (), {
            'pk': self.pk})


    def get_qrcode_data(self):
        return self.get_params_url()



    def getTotal(self):
        return sum([s.getTotal() for s in self.servizi_opzional.all()] + [self.alloggioTotal()])

    def getCaparra(self):
        # La caparra e' il 20% del totale arrotondato a 1 euro
        return D(self.getTotal()*D(0.2)).quantize(D('1'))

    def alloggioTotal(self):
        return self.price+self.iva

    def getDayCount(self):
        day_count = self.event.end-self.event.start
        notti = day_count.days
        return notti

    def getWeekCount(self):
        day_count = self.event.end-self.event.start
        notti = day_count.days
        return notti/7

    def getBasePrice(self):
        return self.price/self.getDayCount()

    def getWeekPrice(self):
        return self.price/self.getWeekCount()

    def delete(self, using=None):
        print 'Reservation.delete'
        if self.event and self.event.id:
            self.event.delete()
        print self.id,self.servizi_opzional.all()
        self.servizi_opzional.all().delete()
        print self.id,self.servizi_opzional.all()
        super(Reservation,self).delete(using)

    def notify_reservation(self):

        # subject = 'Prenotazione alloggio NUM:%s ' % (self.pk)
        # message = " "
        # sender = getattr(settings,'DEFAULT_FROM_EMAIL','from@example.com')

        recipients = getattr(settings, 'SEIPETALI_ADMINS', [])
        recipients = [i[1] for i in recipients]
        notice_type = NoticeType.objects.get(label="new_reservation")
        for mail in recipients:
            try:
                notification_email.EmailBackend(10).deliver_to_recipient_email(mail, None, notice_type,  {"reservation": self})
            except:
                pass

        notification = get_app('notification')
        notification.send([self.user], "new_reservation" , {"reservation": self} )

        # raise Exception('blocca prenotazione')

        # send_mail(subject, message, sender, recipients, fail_silently=False)

                # try:
        # notification = get_app('notification')
        # notification.send(recipients, "new_reservation" , {"reservation": self} )
        # for r in recipients:
        # print

from django.db.models.signals import post_delete,pre_delete


def reservation_delete_callback(sender, **kwargs):
    reservation = kwargs['instance']
    if reservation.event and reservation.event.id:
        reservation.event.delete()
    reservation.servizi_opzional.all().delete()

post_delete.connect(reservation_delete_callback, sender=Reservation)


from django.contrib.auth.signals import user_logged_in
def check_reservation_on_login(sender, request, user,  **kwargs):
    reservation_id = request.session.get('reservation_id',None)
    if reservation_id and user.is_authenticated():
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.user = user
        reservation.save()
        reservation.notify_reservation()

        del request.session['reservation_id']

user_logged_in.connect(check_reservation_on_login)



class Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)




    payment_date = models.DateTimeField()

    PAYMENT_METHOD_BONIFICO = 'bonifico'
    PAYMENT_METHOD_VAGLIA = 'vaglia'
    PAYMENT_METHOD_PAYPAL = 'paypal'
    PAYMENT_METHOD = (
        (PAYMENT_METHOD_BONIFICO,_('Bonifico Bancario')),
        (PAYMENT_METHOD_VAGLIA,_('Vaglia Postale')),
        (PAYMENT_METHOD_PAYPAL,_('Paypal')),
    )

    method = models.CharField(max_length=10,choices=PAYMENT_METHOD,default=PAYMENT_METHOD_PAYPAL)

    reservation = models.ForeignKey(Reservation,null=False,blank=False)


    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False,blank=False)


#################################### Generazione automatica QR-Code ##########################
# Valido sia per la classe Product che ProductProtection
# Se al save l'istanza non ha un qrcode assegnato , viene generato usando ome url get_qrcode_data
def product_post_save(sender, instance, **kwargs):
    if not instance.qr_code and instance.pk:
        qr_code, created = DataQRCode.objects.get_or_create(url=instance.get_qrcode_data())
        qr_code.save()
        instance.qr_code = qr_code
        instance.save()

models.signals.post_save.connect(product_post_save, sender=Reservation)



