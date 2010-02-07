
from south.db import db
from django.db import models
from secret.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'Secret.google_reff'
        # (to signature: django.db.models.fields.CharField(max_length=250, null=True, blank=True))
        db.alter_column('secret_secret', 'google_reff', orm['secret.secret:google_reff'])
        
        # Changing field 'Secret.description'
        # (to signature: django.db.models.fields.TextField(null=True, blank=True))
        db.alter_column('secret_secret', 'description', orm['secret.secret:description'])
        
        # Changing field 'Secret.longitude'
        # (to signature: django.db.models.fields.FloatField(null=True, blank=True))
        db.alter_column('secret_secret', 'longitude', orm['secret.secret:longitude'])
        
        # Changing field 'Secret.latitude'
        # (to signature: django.db.models.fields.FloatField(null=True, blank=True))
        db.alter_column('secret_secret', 'latitude', orm['secret.secret:latitude'])
        
        # Changing field 'Secret.location'
        # (to signature: django.db.models.fields.CharField(max_length=250, null=True, blank=True))
        db.alter_column('secret_secret', 'location', orm['secret.secret:location'])
        
    
    
    def backwards(self, orm):
        
        # Changing field 'Secret.google_reff'
        # (to signature: django.db.models.fields.CharField(max_length=250))
        db.alter_column('secret_secret', 'google_reff', orm['secret.secret:google_reff'])
        
        # Changing field 'Secret.description'
        # (to signature: django.db.models.fields.TextField())
        db.alter_column('secret_secret', 'description', orm['secret.secret:description'])
        
        # Changing field 'Secret.longitude'
        # (to signature: django.db.models.fields.FloatField())
        db.alter_column('secret_secret', 'longitude', orm['secret.secret:longitude'])
        
        # Changing field 'Secret.latitude'
        # (to signature: django.db.models.fields.FloatField())
        db.alter_column('secret_secret', 'latitude', orm['secret.secret:latitude'])
        
        # Changing field 'Secret.location'
        # (to signature: django.db.models.fields.CharField(max_length=250))
        db.alter_column('secret_secret', 'location', orm['secret.secret:location'])
        
    
    
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
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'secret.secret': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator'", 'to': "orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deletor'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'google_reff': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['secret']
