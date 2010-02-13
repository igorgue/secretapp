from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from perm.models import UserContent

class Discussion(UserContent):
    """
    A discussion thread
    """
    title       = models.CharField(max_length=250)
    text        = models.TextField(null=True, blank=True)
    tags        = models.TextField(null=True, blank=True, help_text=_("Comma seperated keywords e.g. pub, family, wifi"))
    pinned      = models.BooleanField(default=False, help_text=_("Will remain at top of discussion board."))
    
    edit_permission = 'Seneschal'
    comments_per_page = 10
    page = 1
    
    def __unicode__(self):
        return self.title
    
    @property
    def pages(self):
        if not hasattr(self, '_pages'):
            self._pages = ((self.comment_count-1)/self.comments_per_page) + 1
        return self._pages
    
    @property
    def xpages(self):
        return xrange(1, self.pages+1)
    
    @property
    def previous_page(self):
        prev = self.page - 1
        return prev if prev > 0 else None
    
    @property
    def next_page(self):
        next = self.page + 1 
        return next if next < self.pages else None
    
    def comments(self):
        "gets all the comments on a discussion - which are not deleted"
        if not hasattr(self, '_comments'):
            from comment.models import DiscussionComment
            # TODO: cache this
            self._comments = DiscussionComment.viewable.filter(discussion=self).select_related()
        return self._comments
    
    @property
    def comment_count(self):
        "gets the comment count"
        if hasattr(self, '_comments'):
            return len(self.comments())
        else:
            if not hasattr(self, '_comment_count'):
                from comment.models import DiscussionComment
                self._comment_count = DiscussionComment.viewable.filter(discussion=self).count()
            return self._comment_count
    
    def page_comments(self):
        "gets the comments on a certain `.page` "
        # works out start and end discussions to be shown
        start = (self.page-1)*self.comments_per_page
        end = self.page*self.comments_per_page
        comments = self.comments()[start:end]
        # assigns editable permissions
        for c in comments:
            c.user_can_edit(self.read_by)
        return comments
    
    def proposals(self):
        if not hasattr(self, '_proposals'):
            from comment.models import Proposal
            # TODO: cache this
            self._proposals = Proposal.viewable.filter(discussion_comment__discussion=self).select_related()
        return self._proposals
    
    @property
    def proposal_count(self):
        if hasattr(self, '_proposals'):
            return len(self.proposals())
        else:
            if not hasattr(self, '_proposal_count'):
                from comment.models import Proposal
                self._proposal_count = Proposal.viewable.filter(discussion_comment__discussion=self).count()
            return self._proposal_count
    
    def safe_title(self):
        "gets the title - safe for use in urls"
        from utilz.manipulators import safe_title
        return safe_title(self.title)
    
    def get_absolute_url(self):
        "gets absolute url - with seo string attached"
        return "%s%s/" % (reverse('view_discussion', kwargs={'pk': self.pk }), self.safe_title())
    
    def get_delete_url(self):
        "gets the url needed to POST to delete the page"
        return reverse('delete_discussion', kwargs={'pk': self.pk})
    
    def get_lastpage_url(self):
        "gets the last page of the discussion"
        return "%s?page=%s" % (self.get_absolute_url(), self.pages)
    
    def __page_of_secret(self, secret):
        "works out which page a certain secret is on"
        from comment.models import SecretComment
        comments = self.comments()
        count = 0
        # ugly but works well with cache (and not used much)
        for c in comments:
            if c.secret == secret:
                break
            count += 1
        return (count/self.comments_per_page) + 1
    
    def set_page_by_secret(self, secret):
        "sets the discussion page by its secret"
        self.page = self.__page_of_secret(secret)
        return self
    
    def get_secretpage_url(self, secret):
        "gets the page of a discussion which a certain secret was mentioned on"
        return "%s?page=%s" (self.get_absolute_url(), self.__page_of_secret(secret))
    
    def lastest_comment(self):
        "gets the latest comment or returns self"
        from comment.models import DiscussionComment
        try:
            return DiscussionComment.viewable.select_related().filter(discussion=self).latest('created_at')
        except DiscussionComment.DoesNotExist:
            return self
