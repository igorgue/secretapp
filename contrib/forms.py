from django import forms

class UserContentForm(forms.ModelForm):
    
    def save(self, request):
        instance = super(self, UserContentForm).save(commit=False)
        instance.created_by = request.user
        instance.ip = request.META['REMOTE_ADDR']
        instance.save()
        return instance