
from south.db import db
from django.db import models
from communication.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'CommunicationTrigger.web_visible'
        db.add_column('communication_communicationtrigger', 'web_visible', orm['communication.communicationtrigger:web_visible'])
        
        # Adding field 'CommunicationTrigger.active'
        db.add_column('communication_communicationtrigger', 'active', orm['communication.communicationtrigger:active'])
        
        # Deleting field 'Communication.web_visable'
        db.delete_column('communication_communication', 'web_visable')
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'CommunicationTrigger.web_visible'
        db.delete_column('communication_communicationtrigger', 'web_visible')
        
        # Deleting field 'CommunicationTrigger.active'
        db.delete_column('communication_communicationtrigger', 'active')
        
        # Adding field 'Communication.web_visable'
        db.add_column('communication_communication', 'web_visable', orm['communication.communication:web_visable'])
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'communication.communication': {
            'body': ('django.db.models.fields.TextField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'failed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {}),
            'trigger': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communication.CommunicationTrigger']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'web': ('django.db.models.fields.TextField', [], {})
        },
        'communication.communicationsetting': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_on': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'trigger': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['communication.CommunicationTrigger']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'communication.communicationtrigger': {
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'optional': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'web_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['communication']
