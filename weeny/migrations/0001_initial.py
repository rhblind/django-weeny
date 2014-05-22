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
            ('seed', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=62, unique=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('weeny', ['WeenySite'])

        # Adding unique constraint on 'WeenySite', fields ['site', 'short_domain']
        db.create_unique('weeny_weenysite', ['site_id', 'short_domain'])

        # Adding model 'WeenyURL'
        db.create_table('weeny_weenyurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contenttype_set_for_weenyurl', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('weeny_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weeny.WeenySite'])),
            ('urlcode', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=10, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('weeny', ['WeenyURL'])

        # Adding unique constraint on 'WeenyURL', fields ['weeny_site', 'urlcode']
        db.create_unique('weeny_weenyurl', ['weeny_site_id', 'urlcode'])


    def backwards(self, orm):
        # Removing unique constraint on 'WeenyURL', fields ['weeny_site', 'urlcode']
        db.delete_unique('weeny_weenyurl', ['weeny_site_id', 'urlcode'])

        # Removing unique constraint on 'WeenySite', fields ['site', 'short_domain']
        db.delete_unique('weeny_weenysite', ['site_id', 'short_domain'])

        # Deleting model 'WeenySite'
        db.delete_table('weeny_weenysite')

        # Deleting model 'WeenyURL'
        db.delete_table('weeny_weenyurl')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'object_name': 'Site', 'ordering': "('domain',)", 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'weeny.weenysite': {
            'Meta': {'object_name': 'WeenySite', 'unique_together': "(['site', 'short_domain'],)"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'default': "'https'", 'max_length': '10'}),
            'seed': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '62', 'unique': 'True', 'blank': 'True'}),
            'short_domain': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        },
        'weeny.weenyurl': {
            'Meta': {'object_name': 'WeenyURL', 'ordering': "['weeny_site']", 'unique_together': "(['weeny_site', 'urlcode'],)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contenttype_set_for_weenyurl'", 'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'urlcode': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'blank': 'True'}),
            'weeny_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weeny.WeenySite']"})
        }
    }

    complete_apps = ['weeny']