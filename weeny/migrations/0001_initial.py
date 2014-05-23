# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WeenySite'
        db.create_table('weeny_weenysite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('short_domain', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('protocol', self.gf('django.db.models.fields.CharField')(default='https', max_length=10)),
            ('track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('seed', self.gf('django.db.models.fields.CharField')(max_length=62, db_index=True, unique=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('weeny', ['WeenySite'])

        # Adding unique constraint on 'WeenySite', fields ['site', 'short_domain']
        db.create_unique('weeny_weenysite', ['site_id', 'short_domain'])

        # Adding model 'WeenyURL'
        db.create_table('weeny_weenyurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], related_name='contenttype_set_for_weenyurl')),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('weeny_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weeny.WeenySite'])),
            ('urlcode', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True, blank=True)),
            ('track', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_revisit', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_visited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('password', self.gf('django.db.models.fields.CharField')(null=True, max_length=128, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('weeny', ['WeenyURL'])

        # Adding unique constraint on 'WeenyURL', fields ['weeny_site', 'urlcode']
        db.create_unique('weeny_weenyurl', ['weeny_site_id', 'urlcode'])

        # Adding model 'UserAgent'
        db.create_table('weeny_useragent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ua_string', self.gf('django.db.models.fields.TextField')()),
            ('browser_family', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('browser_version', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('device_family', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('os_family', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('os_version', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('is_bot', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_mobile', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_pc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_tablet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_touch_capable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('weeny', ['UserAgent'])

        # Adding model 'URLTracking'
        db.create_table('weeny_urltracking', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weeny.WeenyURL'])),
            ('weeny_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weeny.WeenySite'])),
            ('weeny_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('target_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('user_agent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weeny.UserAgent'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('weeny', ['URLTracking'])


    def backwards(self, orm):
        # Removing unique constraint on 'WeenyURL', fields ['weeny_site', 'urlcode']
        db.delete_unique('weeny_weenyurl', ['weeny_site_id', 'urlcode'])

        # Removing unique constraint on 'WeenySite', fields ['site', 'short_domain']
        db.delete_unique('weeny_weenysite', ['site_id', 'short_domain'])

        # Deleting model 'WeenySite'
        db.delete_table('weeny_weenysite')

        # Deleting model 'WeenyURL'
        db.delete_table('weeny_weenyurl')

        # Deleting model 'UserAgent'
        db.delete_table('weeny_useragent')

        # Deleting model 'URLTracking'
        db.delete_table('weeny_urltracking')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'weeny.urltracking': {
            'Meta': {'ordering': "['weeny_url', 'weeny_site__site', 'timestamp', 'user_agent']", 'object_name': 'URLTracking'},
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
            'Meta': {'ordering': "['browser_family', 'os_family', 'browser_version', 'os_version']", 'object_name': 'UserAgent'},
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
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'os_family': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'os_version': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ua_string': ('django.db.models.fields.TextField', [], {})
        },
        'weeny.weenysite': {
            'Meta': {'unique_together': "(['site', 'short_domain'],)", 'object_name': 'WeenySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'default': "'https'", 'max_length': '10'}),
            'seed': ('django.db.models.fields.CharField', [], {'max_length': '62', 'db_index': 'True', 'unique': 'True', 'blank': 'True'}),
            'short_domain': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'track': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'weeny.weenyurl': {
            'Meta': {'unique_together': "(['weeny_site', 'urlcode'],)", 'ordering': "['weeny_site']", 'object_name': 'WeenyURL'},
            'allow_revisit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'contenttype_set_for_weenyurl'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '128', 'blank': 'True'}),
            'track': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'urlcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True', 'blank': 'True'}),
            'weeny_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weeny.WeenySite']"})
        }
    }

    complete_apps = ['weeny']