__author__ = 'elfo'


from django.db import models
from django.core.files import File
from django.core.files.base import ContentFile
import sys
# from localsite.PyQRNative import *
import qrcode
import qrcode.image.svg


from cStringIO import StringIO

class DataQRCode(models.Model):
    url = models.URLField(unique=True)
    qr_image = models.ImageField(
        upload_to="media/qr_codes/url/",
        height_field="qr_image_height",
        width_field="qr_image_width",
        null=True,
        blank=True,
        editable=False
    )
    qr_image_height = models.PositiveIntegerField(null=True, blank=True, editable=False)
    qr_image_width = models.PositiveIntegerField(null=True, blank=True, editable=False)


    def qr_code(self,css_class=None,size=100):
        # css_class = css_class or u''
        return '<img width="%s" class="%s" src="%s">' % (size,css_class ,self.qr_image.url)
    qr_code.allow_tags = True

    def data_size(self):
        return 'char:%s bytes:%s' % (len(self.url), sys.getsizeof(self.url))
    data_size.allow_tags = True

    def qr_info(self):
        qr = qrcode.QRCode(1, qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(self.url,optimize=0)

        return 'best_fit: %s , best_mask_pattern: %s ,  data_list_len: %s , data_cache_len: %s' % ( qr.best_fit(), qr.best_mask_pattern(), len(qr.data_list), len(qr.data_cache))

    qr_info.allow_tags = True



def urlqrcode_pre_save(sender, instance, **kwargs):
    if not hasattr(instance, '_MAKE_QRCODE'):
        instance._MAKE_QRCODE = False
    if instance._MAKE_QRCODE:
        instance._QRCODE = True
    else:
        if not instance.pk:
            instance._QRCODE = True
        else:
            if hasattr(instance, '_QRCODE'):
                instance._QRCODE = False
            else:
                instance._QRCODE = True


def urlqrcode_post_save(sender, instance, **kwargs):
    if instance._QRCODE:
        instance._QRCODE = False
        instance._MAKE_QRCODE = False
        if instance.qr_image:
            instance.qr_image.delete()

        # Il primo valore specifica la versione del qrcode ossia la dimensione minima del qrcode e di conseguenza la capacita di storage
        # il secondo campo indica il fattore di error correction
        #
        # Level L (Low)	7% of codewords can be restored.
        # Level M (Medium)	15% of codewords can be restored.
        # Level Q (Quartile)[39]	25% of codewords can be restored.
        # Level H (High)	30% of codewords can be restored.
        #
        # http://en.wikipedia.org/wiki/QR_code
        # http://blog.qr4.nl/page/QR-Code-Data-Capacity.aspx
        #
        #
        # Di default e' attiva l'opzione auto_fit che adatta la versione del qrcode
        # alla quantita di dati inserita (tenendo presente il fattore di controllo degli error)


        qr = qrcode.QRCode(1, qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(instance.url,optimize=0)
        qr.make()
        image = qr.make_image()

       #Save image to string buffer
        image_buffer = StringIO()
        image.save(image_buffer, kind='PNG')
        image_buffer.seek(0)

       #Here we use django file storage system to save the image.
        file_name = 'UrlQR_%s.png' % instance.id
        file_object = File(image_buffer, file_name)
        content_file = ContentFile(file_object.read())
        instance.qr_image.save(file_name, content_file, save=True)


models.signals.pre_save.connect(urlqrcode_pre_save, sender=DataQRCode)
models.signals.post_save.connect(urlqrcode_post_save, sender=DataQRCode)