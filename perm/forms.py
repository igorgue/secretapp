from django import forms
from django.conf import settings

class UserContentForm(forms.ModelForm):
    facebook_uid = forms.CharField(required=False)
    facebook_first_name = forms.CharField(required=False)
    
    def save(self, request, commit=True):
        instance = super(UserContentForm, self).save(commit=False)
        
        # This is so can assign content to exists users
        if settings.ADMIN_INSERT \
            and 'facebook_uid' in self.cleaned_data \
                and self.cleaned_data['facebook_uid']:
            fuid = self.cleaned_data['facebook_uid']
            # TODO: create a get_or_create a FacebookProfile object
            # if create one, may need to create a User object too
            # FacebookProfile.objects.get_or_create()
        else:
            instance.created_by = request.user
        
        # still want to save the address who created it
        instance.ip = request.META['REMOTE_ADDR']
        if commit:
            instance.save()
        return instance