from contrib.forms import UserContentForm

def SecretForm(UserContentForm):
    class Meta:
        model = Secret
        fields = ('title', 'description', 'location', 'latitude', 'longitude')