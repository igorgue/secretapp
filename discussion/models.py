from django.utils.translation import ugettext_lazy as _
from contrib.models import UserContent

class Discussion(UserContent):
    """
    A discussion thread
    """
    title           = models.CharField(max_length=250)
    text            = models.TextField()
    pinned          = models.BooleanField(default=False, help_text=_("Will remain at top of discussion board."))
    
    page = 1
    
    def page_comments(self, user):
        from comments.models import DiscussionComments
        DiscussionComments.objects.viewable(user).filter(discussion=discussion).order_by('created_at')
    
    def get_absolute_url(self):
        pass
    
    def get_lastpage_url(self):
        pass
    
    def get_secretpage_url(self, secret):
        pass