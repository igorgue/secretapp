from django import forms
from models import *


class UserCommunicationSettingsForm(forms.Form):
    """
    This builds a form for all the settings which are `optional`
            i.e. can be changed by the user
    
    If this setting do not yet exist for that user it is created.
    """
    
    def __init__(self, *args, **kwargs):
        # get user
        if 'user' in kwargs:
            self.user = kwargs['user']
            del kwargs['user']
        else:
            raise KeyError, "UserCommunicationSettingsForm expects `user` as kwargs"
        # setup form
        super(UserCommunicationSettingsForm, self).__init__(*args, **kwargs)
        
        # get all fields which are optional and the users current preferences
        self.options = CommunicationTrigger.objects.filter(optional=True)
        self.preferences = list(CommunicationSetting.objects.filter(user=self.user))
        
        # setup the fields
        for o in self.options:
            pref = self.get_or_create_setting(o)
            self.fields[o.name] = forms.BooleanField(\
                    initial=pref.is_on, required=False, label=o.label, help_text=o.description)
        
        # this is incase its used outside of this app
        try:
            self.action_url = reverse('edit_communication_settings')
        except:
            pass
        
        return
    
    def get_or_create_setting(self, trigger):
        """
        gets the user setting from `self.preferences`
        if DoesNotExist then it creates it and appends to self.preferences
        returns the preference
        """
        pref = filter(lambda p: p.trigger == trigger, self.preferences)
        if len(pref) == 0:
            pref = CommunicationSetting.objects.create(\
                    user=self.user, trigger=trigger, is_on=trigger.default)
            self.preferences.append(pref)
        return pref
    
    def save(self):
        data = self.cleaned_data
        
        # for each of the options
        # it gets the data
        # and sets the pref to the new value
        for o in self.options:
            pref = self.get_or_create_setting(o)
            pref.is_on = data[o.name]
            pref.save()
        
        # returns user
        return self.user

