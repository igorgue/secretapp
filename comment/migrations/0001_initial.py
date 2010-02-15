
from south.db import db
from django.db import models
from comment.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Agreement'
        db.create_table('comment_agreement', (
            ('id', orm['comment.Agreement:id']),
            ('created_by', orm['comment.Agreement:created_by']),
            ('deleted_by_id', orm['comment.Agreement:deleted_by_id']),
            ('created_at', orm['comment.Agreement:created_at']),
            ('updated_at', orm['comment.Agreement:updated_at']),
            ('deleted_at', orm['comment.Agreement:deleted_at']),
            ('deleted', orm['comment.Agreement:deleted']),
            ('approved', orm['comment.Agreement:approved']),
            ('ip', orm['comment.Agreement:ip']),
            ('proposal', orm['comment.Agreement:proposal']),
        ))
        db.send_create_signal('comment', ['Agreement'])
        
        # Adding model 'Proposal'
        db.create_table('comment_proposal', (
            ('id', orm['comment.Proposal:id']),
            ('discussion_comment', orm['comment.Proposal:discussion_comment']),
            ('secret', orm['comment.Proposal:secret']),
        ))
        db.send_create_signal('comment', ['Proposal'])
        
        # Adding model 'DiscussionComment'
        db.create_table('comment_discussioncomment', (
            ('id', orm['comment.DiscussionComment:id']),
            ('created_by', orm['comment.DiscussionComment:created_by']),
            ('deleted_by_id', orm['comment.DiscussionComment:deleted_by_id']),
            ('created_at', orm['comment.DiscussionComment:created_at']),
            ('updated_at', orm['comment.DiscussionComment:updated_at']),
            ('deleted_at', orm['comment.DiscussionComment:deleted_at']),
            ('deleted', orm['comment.DiscussionComment:deleted']),
            ('approved', orm['comment.DiscussionComment:approved']),
            ('ip', orm['comment.DiscussionComment:ip']),
            ('text', orm['comment.DiscussionComment:text']),
            ('discussion', orm['comment.DiscussionComment:discussion']),
        ))
        db.send_create_signal('comment', ['DiscussionComment'])
        
        # Adding model 'ProposalComment'
        db.create_table('comment_proposalcomment', (
            ('id', orm['comment.ProposalComment:id']),
            ('created_by', orm['comment.ProposalComment:created_by']),
            ('deleted_by_id', orm['comment.ProposalComment:deleted_by_id']),
            ('created_at', orm['comment.ProposalComment:created_at']),
            ('updated_at', orm['comment.ProposalComment:updated_at']),
            ('deleted_at', orm['comment.ProposalComment:deleted_at']),
            ('deleted', orm['comment.ProposalComment:deleted']),
            ('approved', orm['comment.ProposalComment:approved']),
            ('ip', orm['comment.ProposalComment:ip']),
            ('text', orm['comment.ProposalComment:text']),
            ('proposal', orm['comment.ProposalComment:proposal']),
        ))
        db.send_create_signal('comment', ['ProposalComment'])
        
        # Adding model 'SecretComment'
        db.create_table('comment_secretcomment', (
            ('id', orm['comment.SecretComment:id']),
            ('created_by', orm['comment.SecretComment:created_by']),
            ('deleted_by_id', orm['comment.SecretComment:deleted_by_id']),
            ('created_at', orm['comment.SecretComment:created_at']),
            ('updated_at', orm['comment.SecretComment:updated_at']),
            ('deleted_at', orm['comment.SecretComment:deleted_at']),
            ('deleted', orm['comment.SecretComment:deleted']),
            ('approved', orm['comment.SecretComment:approved']),
            ('ip', orm['comment.SecretComment:ip']),
            ('text', orm['comment.SecretComment:text']),
            ('secret', orm['comment.SecretComment:secret']),
        ))
        db.send_create_signal('comment', ['SecretComment'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Agreement'
        db.delete_table('comment_agreement')
        
        # Deleting model 'Proposal'
        db.delete_table('comment_proposal')
        
        # Deleting model 'DiscussionComment'
        db.delete_table('comment_discussioncomment')
        
        # Deleting model 'ProposalComment'
        db.delete_table('comment_proposalcomment')
        
        # Deleting model 'SecretComment'
        db.delete_table('comment_secretcomment')
        
    
    
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
        'comment.agreement': {
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comment.Proposal']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'comment.discussioncomment': {
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['discussion.Discussion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'secrets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['secret.Secret']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'comment.proposal': {
            'discussion_comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comment.DiscussionComment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'secret': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['secret.Secret']"})
        },
        'comment.proposalcomment': {
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'proposal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['comment.Proposal']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'comment.secretcomment': {
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['secret.Secret']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'discussion.discussion': {
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'pinned': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'tags': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'secret.secret': {
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
    
    complete_apps = ['comment']
