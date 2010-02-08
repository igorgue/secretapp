from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from contrib.models import UserContent

class Discussion(UserContent):
    """
    A discussion thread
    """
    title       = models.CharField(max_length=250)
    text        = models.TextField()
    pinned      = models.BooleanField(default=False, help_text=_("Will remain at top of discussion board."))
    
    comments_per_page = 10
    page = 1
    
    def comments(self):
        from comment.models import DiscussionComment
        # TODO: cache this
        return DiscussionComments.objects.viewable().filter(discussion=self)
    
    def safe_title(self):
        # TODO: make this more robust
        return self.title.replace(' ', '+')
    
    def get_absolute_url(self):
        # gets absolute url - with seo string attached
        return "%s%s/" % (reverse('view_discussion', {'pk': self.pk }), self.safe_title())
    
    def get_lastpage_url(self):
        # gets the last page of the discussion
        lastpage = (len(comments)/self.comments_per_page) + 1
        return "%s?page=%s" % (self.get_absolute_url(), lastpage)
    
    def get_secretpage_url(self, secret):
        # gets the page of a discussion which a certain secret was mentioned on
        from comment.models import SecretComment
        comments = self.comments()
        count = 0
        # ugly but works well with cache (and not used much)
        for c in len(comments):
            if c.secret = secret:
                break
            count += 1
        page = (count/self.comments_per_page) + 1
        return "%s?page=%s" (self.get_absolute_url(), page)


