from django import forms
from models import *

class UserSettingsForm(forms.ModelForm):
    
    class Meta:
        model = UserSettings
        fields = ('publish_to_wall', )