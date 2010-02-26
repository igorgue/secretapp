from django.contrib import admin
from models import * 

class UploadedPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail', 'caption', 'deleted', 'approved', 'created_at',)
    list_editable = ('approved', 'deleted')
    
    def thumbnail(self, instance):
        try:
            return "<img src='%s' /> original:%sx%s, resized:%sx%s" % \
                (instance.thumb.url, instance.original.width, instance.original.height, \
                                            instance.resized.width, instance.resized.height)
        except:
            return "Error finding file"
    thumbnail.allow_tags = True
    thumbnail.short_description = 'image'

admin.site.register(UploadedPhoto, UploadedPhotoAdmin)