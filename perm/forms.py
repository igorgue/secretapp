from django import forms
from django.conf import settings
from django.contrib.auth.models import User

class UserContentForm(forms.ModelForm):
    facebook_uid = forms.CharField(required=False, help_text="Right click on the user name. Copy link address. Paste here.")
    facebook_name = forms.CharField(required=False, help_text="Write the firstname or initials of user here.")
    
    def save(self, request, commit=True):
        instance = super(UserContentForm, self).save(commit=False)
        
        # This is so can assign content to exists users
        if settings.ADMIN_INSERT and 'facebook_uid' in self.cleaned_data and self.cleaned_data['facebook_uid']:
            
            # take the user url and convert to fuid - so they can claim later
            fuid = self.cleaned_data['facebook_uid'].replace('http://www.facebook.com/profile.php?id=', '')
            
            from facebook import Facebook
            fb_user, is_new = User.objects.get_or_create(username='FB:%s' % fuid, first_name=self.cleaned_data['facebook_name'])
            instance.created_by = fb_user
            
        else:
            instance.created_by = request.user
        
        # still want to save the address who created it
        instance.ip = request.META['REMOTE_ADDR']
        if commit:
            instance.save()
        return instance