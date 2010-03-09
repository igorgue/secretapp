from django.contrib import admin
from models import * 

class CommunicationTriggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'label', 'default', 'optional', 'active', 'web_visible')
    list_filter = ('active', 'optional', 'web_visible')
    list_editable = ('active', 'web_visible')
    search_fields = ('name', 'label',)
admin.site.register(CommunicationTrigger, CommunicationTriggerAdmin)

class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'trigger', 'user', 'sent', 'read', 'deleted', 'failed',)
    list_filter = ('sent', 'read', 'deleted', 'failed',)
    list_editable = ('deleted',)
    search_fields = ('title', 'text', 'tags')
admin.site.register(Communication, CommunicationAdmin)