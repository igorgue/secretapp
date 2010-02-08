from django.core.urlresolvers import reverse
from contrib.forms import UserContentForm

def SecretForm(UserContentForm):
    class Meta:
        model = Secret
        fields = ('title', 'description', 'location', 'latitude', 'longitude')
    
    def set_url(self, secret):
        self.Meta.url = reverse('edit_secret', {'pk': secret.pk})