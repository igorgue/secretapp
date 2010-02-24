from django import forms
from perm.forms import UserContentForm
from models import *


class UploadPhotoForm(UserContentForm):
    image = forms.ImageField()
    caption = forms.CharField(required=False)
    
    class Meta:
        model = UploadedPhoto
        fields = ('caption',)
    
    def save(self, request, commit=False):
        instance = super(UploadPhotoForm, self).save(request, commit=False)
        instance.secret = self.secret
        instance.save()
        instance.save_files(self.cleaned_data['image'])
        return instance
























