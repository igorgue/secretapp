from django import forms

class UserContentForm(forms.ModelForm):
    
    def save(self, request, commit=True):
        instance = super(self, UserContentForm).save(commit=False)
        instance.created_by = request.user
        instance.ip = request.META['REMOTE_ADDR']
        if commit:
            instance.save()
        return instance