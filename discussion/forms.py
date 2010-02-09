from perm.forms import UserContentForm
from models import *

class DiscussionForm(UserContentForm):
    class Meta:
        model = Discussion
        fields = ('title', 'text',)