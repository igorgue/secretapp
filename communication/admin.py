from django.contrib import admin
from models import * 

class CommunicationTriggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'label', 'default', 'optional', 'active',)
    list_filter = ('active', 'optional',)
    list_editable = ('active',)
    search_fields = ('name', 'label',)
admin.site.register(CommunicationTrigger, CommunicationTriggerAdmin)

class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'trigger', 'sent', 'read', 'deleted', 'failed', 'web_visible',)
    list_filter = ('sent', 'read', 'deleted', 'failed', 'web_visible')
    list_editable = ('deleted',)
    search_fields = ('title', 'text', 'tags')
admin.site.register(Communication, CommunicationAdmin)