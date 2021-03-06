from django import forms
from django.core.urlresolvers import reverse
from perm.forms import UserContentForm
from models import *


class UploadPhotoForm(UserContentForm):
    image = forms.ImageField()
    caption = forms.CharField(required=False)
    
    class Meta:
        model = UploadedPhoto
        fields = ('caption',)
        id = 'uploadphoto'
    
    def save(self, request, commit=False):
        instance = super(UploadPhotoForm, self).save(request, commit=False)
        instance.secret = self.secret
        instance.save()
        try:
            instance.save_files(self.cleaned_data['image'])
        except:
            # if it fails to save, we want to delete the image
            instance.deleted = True
            instance.save()
        return instance

    def set_url(self, secret):
        self.action_url = reverse('upload_photo', kwargs={'secret_id': secret.id})
        return self




