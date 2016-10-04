# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Address.unformatted'
        db.add_column(u'address_address', 'unformatted',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


        # Changing field 'Address.street_number'
        db.alter_column(u'address_address', 'street_number', self.gf('django.db.models.fields.CharField')(max_length=6, null=True))

        # Changing field 'Address.locality'
        db.alter_column(u'address_address', 'locality_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['address.Locality']))

        # Changing field 'Address.street_address'
        db.alter_column(u'address_address', 'street_address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    def backwards(self, orm):
        # Deleting field 'Address.unformatted'
        db.delete_column(u'address_address', 'unformatted')


        # Changing field 'Address.street_number'
        db.alter_column(u'address_address', 'street_number', self.gf('django.db.models.fields.CharField')(default='', max_length=6))

        # Changing field 'Address.locality'
        db.alter_column(u'address_address', 'locality_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['address.Locality']))

        # Changing field 'Address.street_address'
        db.alter_column(u'address_address', 'street_address', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

    models = {
        u'address.address': {
            'Meta': {'ordering': "('locality', 'street_address')", 'object_name': 'Address'},
            'formatted': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'addresses'", 'null': 'True', 'to': u"orm['address.Locality']"}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'street_number': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'unformatted': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'address.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'blank': 'True'})
        },
        u'address.locality': {
            'Meta': {'ordering': "('state', 'name')", 'unique_together': "(('name', 'state'),)", 'object_name': 'Locality'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '165', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'localities'", 'to': u"orm['address.State']"})
        },
        u'address.state': {
            'Meta': {'ordering': "('country', 'name')", 'unique_together': "(('name', 'country'),)", 'object_name': 'State'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'states'", 'to': u"orm['address.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '165', 'blank': 'True'})
        }
    }

    complete_apps = ['address']