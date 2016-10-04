__author__ = 'elfo'

from django.contrib import admin
from models import DataQRCode

class DataQRCodeAdmin(admin.ModelAdmin):
    list_display = ('url','data_size','qr_info','qr_image_width','qr_image_height', 'qr_code')

admin.site.register(DataQRCode, DataQRCodeAdmin)