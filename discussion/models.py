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
        from contrib.utils import safe_title
        return safe_title(self.title)
    
    def get_absolute_url(self):
        # gets absolute url - with seo string attached
        return "%s%s/" % (reverse('view_discussion', {'pk': self.pk }), self.safe_title())
    
    def get_lastpage_url(self):
        # gets the last page of the discussion
        lastpage = (len(comments)/self.comments_per_page) + 1
        return "%s?page=%s" % (self.get_absolute_url(), lastpage)
    
    def __page_of_secret(self, secret):
        from comment.models import SecretComment
        comments = self.comments()
        count = 0
        # ugly but works well with cache (and not used much)
        for c in len(comments):
            if c.secret = secret:
                break
            count += 1
        return (count/self.comments_per_page) + 1
    
    def set_page_by_secret(self, secret):
        # sets the discussion page by its secret
        self.page = self.__page_of_secret(secret)
        return self
    
    def get_secretpage_url(self, secret):
        # gets the page of a discussion which a certain secret was mentioned on
        return "%s?page=%s" (self.get_absolute_url(), self.__page_of_secret(secret))


