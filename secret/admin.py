from django.contrib import admin
from models import * 
from comment.models import SecretComment
from comment.models import Proposal

class SecretCommentInline(admin.StackedInline):
    model = SecretComment
    
class SecretAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'deleted', 'approved', 'created_at',)
    list_filter = ('approved', 'deleted',)
    list_editable = ('approved', 'deleted')
    inlines = [
               SecretCommentInline,
               ]
admin.site.register(Secret, SecretAdmin)