from django.contrib import admin
from models import * 

admin.site.register(SecretComment)

class DiscussionCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'discussion', 'text', 'deleted', 'approved', 'created_at',)
    list_filter = ('approved', 'deleted',)
    list_editable = ('approved', 'deleted')
    search_fields = ('discussion__title', 'text')
admin.site.register(DiscussionComment, DiscussionCommentAdmin)

admin.site.register(Proposal)
admin.site.register(ProposalComment)
admin.site.register(Agreement)

