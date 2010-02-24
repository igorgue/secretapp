from django import forms
from django.core.files.base import ContentFile
from perm.forms import UserContentForm
from PIL import Image, ImageOps, ImageEnhance
from models import *

#class ImageHandler(object):
#    def __init__(self, image):
#        # save depending on type
#        if isinstance(image, ImageHandler):
#            self.orig = image.orig
#            self.file = image.file
#        elif hasattr(image, '_Image__transformer'):
#            self.orig = None
#            self.file = image
#        else:
#            self.orig = image
#            self.file = Image.open(image)
#        
#        self.file = fle
#        # want this to be handled once
#        self.handle_exif_rotation()
#    
#    def rotate(self, rotation):
#        """ Takes rotation angle in clockwise degrees int """
#        self.file = self.file.rotate(rotation)
#        return self
#    
#    def resize(self, max_size):
#        """ Takes max_size as a tuple(int, int) of width,height in pixels """
#        im = self.file
#        self.file = ImageOps.fit(im, max_size, Image.ANTIALIAS, 0, (0.5,0.5))
#        return self
#    
#    def content(self):
#        """ Returns the contents of the file """
#        return self.file.content
#    
#    def handle_exif_rotation(self):
#        """
#        Handles rotating the exif data to the correct angle
#        """
#        try:
#            orientation_tag = 274
#            orientation_angles = {
#                1: 0,
#                6: 90,
#                8: 270,
#            }
#            exif = self.file._getexif()
#            if exif:
#                rotation = orientation_angles[exif[orientation_tag]]
#                if rotation:
#                    # its been rotated by rotation already, so want to rotate back
#                    self.rotate(-rotation)
#        except:
#            pass
#
#
#
class UploadPhotoForm(UserContentForm):
    image = forms.ImageField()
    text = forms.CharField(required=False)
    
    class Meta(UserContent.Meta):
        model = TestPhoto
        fields = ('image',)
    
    def save(self, request):
        instance = super(UploadPhotoForm, self).save(request, commit=False)
        i = self.cleaned_data['image']
        




























