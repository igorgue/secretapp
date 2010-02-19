from django import forms
from models import *

class UserSettingsForm(forms.Form):
    email = forms.EmailField(required=False)
    publish_to_wall = forms.BooleanField(required=False)
    
    def save(self, *args, **kwargs):
        # settings file
        if 'publish_to_wall' in self.cleaned_data:
            us, new = UserSettings.objects.get_or_create(user=self.user)
            us.publish_to_wall = self.cleaned_data['publish_to_wall']
            us.save()
        # user profile
        if 'email' in self.cleaned_data and self.cleaned_data['email']:
            user.email = self.cleaned_data['email']
            user.save()
        return conf