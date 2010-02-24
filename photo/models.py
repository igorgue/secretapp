from django.conf import settings
from django.db import models
from perm.models import UserContent
from django.core.files.storage import FileSystemStorage
from storage import BotoS3Storage

#if settings.DEBUG:
#    fs = FileSystemStorage()
#else:
#fs = BotoS3Storage(bucket="secret-test", base="photos")


class TestPhoto(UserContent):
    """
    A photo uploaded by a user from their computer
    """
    image = models.ImageField(upload_to="uploaded/images/%Y%m%d", blank=True, editable=False)
     