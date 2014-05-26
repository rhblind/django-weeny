# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WeenyURL.is_removed'
        db.add_column('weeny_weenyurl', 'is_removed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'WeenySite.redirect_short_domain'
        db.add_column('weeny_weenysite', 'redirect_short_domain',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'WeenySite.requires_moderation'
        db.add_column('weeny_weenysite', 'requires_moderation',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WeenyURL.is_removed'
        db.delete_column('weeny_weenyurl', 'is_removed')

        # Deleting field 'WeenySite.redirect_short_domain'
        db.delete_column('weeny_weenysite', 'redirect_short_domain')

        # Deleting field 'WeenySite.requires_moderation'
        db.delete_column('weeny_weenysite', 'requires_moderation')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'db_table': "'django_site'", 'ordering': "('domain',)"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'weeny.urltracking': {
            'Meta': {'object_name': 'URLTracking', 'ordering': "['weeny_url', 'weeny_site__site', 'timestamp', 'user_agent']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'target_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weeny.WeenyURL']"}),
            'user_agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weeny.UserAgent']"}),
            'weeny_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weeny.WeenySite']"}),
            'weeny_url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'weeny.useragent': {
            'Meta': {'object_name': 'UserAgent', 'ordering': "['browser_family', 'os_family', 'browser_version', 'os_version']"},
            'browser_family': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'browser_version': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'device_family': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_bot': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_pc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_tablet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_touch_capable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'os_family': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'os_version': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ua_string': ('django.db.models.fields.TextField', [], {})
        },
        'weeny.weenysite': {
            'Meta': {'object_name': 'WeenySite', 'unique_together': "(['site', 'short_domain'],)"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': "'https'"}),
            'redirect_short_domain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'requires_moderation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'seed': ('django.db.models.fields.CharField', [], {'max_length': '62', 'db_index': 'True', 'unique': 'True', 'blank': 'True'}),
            'short_domain': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'track': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'weeny.weenyurl': {
            'Meta': {'object_name': 'WeenyURL', 'ordering': "['weeny_site']", 'unique_together': "(['weeny_site', 'urlcode'],)"},
            'allow_revisit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'contenttype_set_for_weenyurl'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True', 'null': 'True'}),
            'track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'urlcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True', 'db_index': 'True'}),
            'weeny_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weeny.WeenySite']"})
        }
    }

    complete_apps = ['weeny']