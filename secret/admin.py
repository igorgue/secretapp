from django.contrib import admin
from models import * 
from comment.models import SecretComment
from comment.models import Proposal

class SecretCommentInline(admin.StackedInline):
    model = SecretComment
    
class SecretAdmin(admin.ModelAdmin):
    inlines = [
               SecretCommentInline,
               ]
admin.site.register(Secret, SecretAdmin)