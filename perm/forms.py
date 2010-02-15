from django import forms
from django.conf import settings
from django.contrib.auth.models import User

class UserContentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserContentForm, self).__init__(*args, **kwargs)
        self.Meta.exclude = ('approved',)
    
    def save(self, request, commit=True):
        instance = super(UserContentForm, self).save(commit=False)
        
        instance.created_by = request.user
        instance.ip = request.META['REMOTE_ADDR'] if 'REMOTE_ADDR' in request.META else None
        
        # only commit is want to
        if commit:
            instance.save()
        return instance