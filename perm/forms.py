from django import forms
from django.conf import settings
from django.contrib.auth.models import User

class UserContentForm(forms.ModelForm):
    def __init__(self, data=None, permission_level=0, *args, **kwargs):
        super(UserContentForm, self).__init__(data, *args, **kwargs)
        self.Meta.exclude = ('approved',)
        
        if permission_level > 2:
            if 'instance' in kwargs:
                instance = kwargs['instance']
                user = instance.created_by
            self.use_facebook = True
            self.fields['facebook_uid'] = forms.CharField(initial=user.username.replace('FB:', ''), required=False, help_text="Right click on the user name. Copy link address. Paste here.")
            self.fields['facebook_name'] = forms.CharField(initial=user.first_name, required=False, help_text="Write the firstname or initials of user here.")
        else:
            self.use_facebook = False
        
    
    def save(self, request, commit=True):
        instance = super(UserContentForm, self).save(commit=False)
        instance.created_by = request.user
        
        if self.use_facebook and 'facebook_uid' in self.cleaned_data and self.cleaned_data['facebook_uid']:
            # take the user url and convert to fuid - so they can claim later
            fuid = self.cleaned_data['facebook_uid'].replace('http://www.facebook.com/profile.php?id=', '')
            from facebook import Facebook
            fb_user, is_new = User.objects.get_or_create(username='FB:%s' % fuid)
            if 'facebook_name' in self.cleaned_data:
                fb_user.first_name = self.cleaned_data['facebook_name']
                fb_user.save()
            instance.created_by = fb_user
        else:
            instance.created_by = request.user
        
        instance.ip = request.META['REMOTE_ADDR'] if 'REMOTE_ADDR' in request.META else None
        
        # only commit is want to
        if commit:
            instance.save()
        return instance