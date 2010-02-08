from django.core.urlresolvers import reverse
from perm.forms import UserContentForm

def SecretForm(UserContentForm):
    class Meta:
        model = Secret
        fields = ('title', 'description', 'location', 'latitude', 'longitude')
    
    def set_url(self, secret=None, discussion=None):
        # handling data input
        if hasattr(secret, 'pk') and secret.pk:
            secret_id = secret.pk
        else:
            secret_id = None
        if isinstance(dicussion, Discussion):
            discussion_id = discussion.pk
        else:
            try:
                discussion_id = int(discussion)
            except:
                discussion_id = None
        
        # handle options
        if dicussion_id and not secret_id:
            self.Meta.url = reverse('new_secret_for_discussion', {'discussion_id': discussion_id})
        elif not discussion_id and secret_id:
            self.Meta.url = reverse('edit_secret', {'pk': secret_id })
        else:
            self.Meta.url = reverse('new_secret')