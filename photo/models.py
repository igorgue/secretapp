from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models

from secret.models import Secret
from perm.models import UserContent
from storage import BotoS3Storage
from handler import ImageHandler

if settings.DEBUG:
    def monkey_url(self, name):
        return "/".join((settings.MEDIA_URL, name))
    # monkey patching store - so url point directly to media (no messing)
    FileSystemStorage.url = monkey_url
    photo_storage = FileSystemStorage()
    upload_to = "uploaded/images"
else:
    photo_storage = BotoS3Storage(bucket="secret-uploads", base="photos")
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
    resized_proportions = (900, 700)
    thumb_proportions = (150, 150)
    
    def save_files(self, image_content):
        original = ImageHandler(image_content)
        # save original
        self.original.save("o_%s.%s" % (self.pk, self.extension), original.content_file())
        # save resize
        resized = original.resize(self.resized_proportions)
        self.resized.save("%s.%s" % (self.pk, self.extension), resized.content_file())
        # save thumb
        thumb = original.fit(self.thumb_proportions)
        self.thumb.save("t_%s.%s" % (self.pk, self.extension), thumb.content_file())
        return self