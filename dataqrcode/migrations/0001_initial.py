# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataQRCode'
        db.create_table(u'dataqrcode_dataqrcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('qr_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('qr_image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('qr_image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dataqrcode', ['DataQRCode'])


    def backwards(self, orm):
        # Deleting model 'DataQRCode'
        db.delete_table(u'dataqrcode_dataqrcode')


    models = {
        u'dataqrcode.dataqrcode': {
            'Meta': {'object_name': 'DataQRCode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qr_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qr_image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qr_image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['dataqrcode']