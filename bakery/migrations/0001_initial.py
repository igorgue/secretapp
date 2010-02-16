
from south.db import db
from django.db import models
from bakery.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UrlCache'
        db.create_table('bakery_urlcache', (
            ('id', orm['bakery.UrlCache:id']),
            ('path', orm['bakery.UrlCache:path']),
            ('value', orm['bakery.UrlCache:value']),
            ('content_type', orm['bakery.UrlCache:content_type']),
            ('expire_after', orm['bakery.UrlCache:expire_after']),
            ('updated', orm['bakery.UrlCache:updated']),
            ('created', orm['bakery.UrlCache:created']),
        ))
        db.send_create_signal('bakery', ['UrlCache'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UrlCache'
        db.delete_table('bakery_urlcache')
        
    
    
    models = {
        'bakery.urlcache': {
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expire_after': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }
    
    complete_apps = ['bakery']
