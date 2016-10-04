# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NoticeType'
        db.create_table(u'notification_noticetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('default', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'notification', ['NoticeType'])

        # Adding model 'NoticeSetting'
        db.create_table(u'notification_noticesetting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('notice_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notification.NoticeType'])),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('send', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'notification', ['NoticeSetting'])

        # Adding unique constraint on 'NoticeSetting', fields ['user', 'notice_type', 'medium']
        db.create_unique(u'notification_noticesetting', ['user_id', 'notice_type_id', 'medium'])

        # Adding model 'NoticeQueueBatch'
        db.create_table(u'notification_noticequeuebatch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pickled_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'notification', ['NoticeQueueBatch'])


    def backwards(self, orm):
        # Removing unique constraint on 'NoticeSetting', fields ['user', 'notice_type', 'medium']
        db.delete_unique(u'notification_noticesetting', ['user_id', 'notice_type_id', 'medium'])

        # Deleting model 'NoticeType'
        db.delete_table(u'notification_noticetype')

        # Deleting model 'NoticeSetting'
        db.delete_table(u'notification_noticesetting')

        # Deleting model 'NoticeQueueBatch'
        db.delete_table(u'notification_noticequeuebatch')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'notification.noticequeuebatch': {
            'Meta': {'object_name': 'NoticeQueueBatch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickled_data': ('django.db.models.fields.TextField', [], {})
        },
        u'notification.noticesetting': {
            'Meta': {'unique_together': "(('user', 'notice_type', 'medium'),)", 'object_name': 'NoticeSetting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'notice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['notification.NoticeType']"}),
            'send': ('django.db.models.fields.BooleanField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'notification.noticetype': {
            'Meta': {'object_name': 'NoticeType'},
            'default': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['notification']