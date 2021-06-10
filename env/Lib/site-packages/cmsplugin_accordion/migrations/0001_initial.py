# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccordionPlugin'
        db.create_table('cmsplugin_accordionplugin', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('cmsplugin_accordion', ['AccordionPlugin'])

        # Adding model 'AccordionRow'
        db.create_table('cmsplugin_accordion_accordionrow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accordion', self.gf('django.db.models.fields.related.ForeignKey')(related_name='accordion_rows', to=orm['cmsplugin_accordion.AccordionPlugin'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Placeholder'], null=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('cmsplugin_accordion', ['AccordionRow'])


    def backwards(self, orm):
        # Deleting model 'AccordionPlugin'
        db.delete_table('cmsplugin_accordionplugin')

        # Deleting model 'AccordionRow'
        db.delete_table('cmsplugin_accordion_accordionrow')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'cmsplugin_accordion.accordionplugin': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AccordionPlugin', 'db_table': "'cmsplugin_accordionplugin'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'cmsplugin_accordion.accordionrow': {
            'Meta': {'ordering': "('accordion__name', 'position', 'title')", 'object_name': 'AccordionRow'},
            'accordion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accordion_rows'", 'to': "orm['cmsplugin_accordion.AccordionPlugin']"}),
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['cmsplugin_accordion']
