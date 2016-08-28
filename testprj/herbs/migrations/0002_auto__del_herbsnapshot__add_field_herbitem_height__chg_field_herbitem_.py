# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'HerbSnapshot'
        db.delete_table(u'herbs_herbsnapshot')

        # Adding field 'HerbItem.height'
        db.add_column(u'herbs_herbitem', 'height',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)


        # Changing field 'HerbItem.identified_s'
        db.alter_column(u'herbs_herbitem', 'identified_s', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'HerbItem.identified_e'
        db.alter_column(u'herbs_herbitem', 'identified_e', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'HerbItem.collected_e'
        db.alter_column(u'herbs_herbitem', 'collected_e', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'HerbItem.collected_s'
        db.alter_column(u'herbs_herbitem', 'collected_s', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):
        # Adding model 'HerbSnapshot'
        db.create_table(u'herbs_herbsnapshot', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('image', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'herbs', ['HerbSnapshot'])

        # Deleting field 'HerbItem.height'
        db.delete_column(u'herbs_herbitem', 'height')


        # User chose to not deal with backwards NULL issues for 'HerbItem.identified_s'
        raise RuntimeError("Cannot reverse this migration. 'HerbItem.identified_s' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'HerbItem.identified_s'
        db.alter_column(u'herbs_herbitem', 'identified_s', self.gf('django.db.models.fields.DateField')())

        # User chose to not deal with backwards NULL issues for 'HerbItem.identified_e'
        raise RuntimeError("Cannot reverse this migration. 'HerbItem.identified_e' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'HerbItem.identified_e'
        db.alter_column(u'herbs_herbitem', 'identified_e', self.gf('django.db.models.fields.DateField')())

        # Changing field 'HerbItem.collected_e'
        db.alter_column(u'herbs_herbitem', 'collected_e', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2016, 8, 28, 0, 0)))

        # Changing field 'HerbItem.collected_s'
        db.alter_column(u'herbs_herbitem', 'collected_s', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2016, 8, 28, 0, 0)))

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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'herbs.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'})
        },
        u'herbs.errorlog': {
            'Meta': {'ordering': "('-created', 'message')", 'object_name': 'ErrorLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'})
        },
        u'herbs.family': {
            'Meta': {'object_name': 'Family'},
            'authorship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['herbs.Author']", 'null': 'True', 'through': u"orm['herbs.FamilyAuthorship']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'})
        },
        u'herbs.familyauthorship': {
            'Meta': {'object_name': 'FamilyAuthorship'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbs.Author']", 'null': 'True', 'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbs.Family']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'herbs.genus': {
            'Meta': {'object_name': 'Genus'},
            'authorship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['herbs.Author']", 'null': 'True', 'through': u"orm['herbs.GenusAuthorship']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'})
        },
        u'herbs.genusauthorship': {
            'Meta': {'object_name': 'GenusAuthorship'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbs.Author']", 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbs.Genus']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'herbs.herbitem': {
            'Meta': {'ordering': "('family', 'genus', 'species')", 'object_name': 'HerbItem'},
            'collected_e': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'collected_s': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'collectedby': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'coordinates': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'createdby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'detailed': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'ecodescr': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbs.Family']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'gcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbs.Genus']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'height': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identified_e': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'identified_s': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'identifiedby': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'itemcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'}),
            'place': ('geoposition.fields.GeopositionField', [], {'max_length': '42', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'region': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbs.Species']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'uhash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updatedby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'herbs.loadedfiles': {
            'Meta': {'ordering': "('created', 'status', 'createdby')", 'object_name': 'LoadedFiles'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'createdby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'datafile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'herbs.pendingherbs': {
            'Meta': {'ordering': "('family', 'genus', 'species')", 'object_name': 'PendingHerbs', 'db_table': "'herbs_loadpendingherbs'", '_ormbases': [u'herbs.HerbItem']},
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'err_msg': ('django.db.models.fields.TextField', [], {'default': 'True', 'blank': 'True'}),
            u'herbitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['herbs.HerbItem']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'herbs.species': {
            'Meta': {'object_name': 'Species'},
            'authorship': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['herbs.Author']", 'null': 'True', 'through': u"orm['herbs.SpeciesAuthorship']", 'blank': 'True'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbs.Genus']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'})
        },
        u'herbs.speciesauthorship': {
            'Meta': {'object_name': 'SpeciesAuthorship'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbs.Author']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['herbs.Species']"})
        }
    }

    complete_apps = ['herbs']