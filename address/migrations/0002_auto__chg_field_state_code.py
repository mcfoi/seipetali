# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'State.code'
        db.alter_column(u'address_state', 'code', self.gf('django.db.models.fields.CharField')(max_length=3, null=True))

    def backwards(self, orm):

        # Changing field 'State.code'
        db.alter_column(u'address_state', 'code', self.gf('django.db.models.fields.CharField')(default='', max_length=3))

    models = {
        u'address.address': {
            'Meta': {'ordering': "('locality', 'street_address')", 'object_name': 'Address'},
            'formatted': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'locality': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addresses'", 'to': u"orm['address.Locality']"}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'street_number': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'})
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