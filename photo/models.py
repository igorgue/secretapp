from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models

from secret.models import Secret
from perm.models import UserContent
from storage import BotoS3Storage
from handler import ImageHandler

#if settings.DEBUG:
#   fs = FileSystemStorage()
#   upload_to = "uploaded/images"
#else:
photo_storage = BotoS3Storage(bucket="secret-test", base="photos")
upload_to = "uploaded"

class UploadedPhoto(UserContent):
    """
    A generic photo uploaded by a user from their computer
    """
    secret      = models.ForeignKey(Secret)
    original    = models.ImageField(upload_to=upload_to, blank=True, editable=False, storage=photo_storage)
    resized     = models.ImageField(upload_to=upload_to, blank=True, editable=False, storage=photo_storage)
    thumb       = models.ImageField(upload_to=upload_to, blank=True, editable=False, storage=photo_storage)
    caption     = models.TextField(blank=True, null=True)
    
    extension = 'jpeg'
    resized_proportions = (600,400)
    thumb_proportions = (50,50)
    
    def save_files(self, image_content):
        handler = ImageHandler(image_content)
        # save original
        self.original.save("o_%s.%s" % (self.pk, self.extension), handler.content_file())
        # save resize
        handler.resize(self.resized_proportions)
        self.resized.save("%s.%s" % (self.pk, self.extension), handler.content_file())
        # save thumb
        handler.resize(self.thumb_proportions)
        self.thumb.save("t_%s.%s" % (self.pk, self.extension), handler.content_file())
        return self