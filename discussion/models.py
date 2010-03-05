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
    comments_per_page = 5
    page = 1
    
    # PAGES
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
        return next if next <= self.pages else None
    
    # COMMENTS
    def comments(self):
        "gets all the comments on a discussion - which are not deleted"
        if not hasattr(self, '_comments'):
            from comment.models import DiscussionComment
            # TODO: cache this
            self._comments = DiscussionComment.viewable.filter(discussion=self).select_related()
        return self._comments
    
    @property
    def comment_count(self):
        from comment.models import DiscussionComment
        return DiscussionComment.viewable.filter(discussion=self).count()
    
    def page_comments(self):
        "gets the comments on a certain `.page` "
        # works out start and end discussions to be shown
        # add 1 to filter out first comment, which is discussion post itself
        start = (self.page-1)*self.comments_per_page
        end = self.page*self.comments_per_page + 1
        comments = self.comments()[start:end]
        # assigns editable permissions
        for c in comments:
            c.user_can_edit(self.read_by)
        return comments
    
    def latest_comment(self):
        "gets the latest comment or returns self"
        from comment.models import DiscussionComment
        try:
            return DiscussionComment.viewable.select_related().filter(discussion=self).latest('created_at')
        except DiscussionComment.DoesNotExist:
            return self
    
    # PROPOSALS
    def proposals(self):
        if not hasattr(self, '_proposals'):
            from comment.models import Proposal
            # TODO: cache this
            self._proposals = Proposal.viewable.filter(discussion_comment__discussion=self).select_related()
        return self._proposals
    
    @property
    def proposal_count(self):
        from comment.models import Proposal
        return Proposal.viewable.filter(discussion_comment__discussion=self).count()
    
    # URLS
    def safe_title(self):
        "gets the title - safe for use in urls"
        from utilz.manipulators import safe_title
        return safe_title(self.title)
    
    def get_absolute_url(self):
        "gets absolute url - with seo string attached"
        return "%s%s/" % (reverse('view_discussion', kwargs={'pk': self.pk }), self.safe_title())
    
    def get_edit_url(self):
        "gets the url needed to edit the page"
        return reverse('edit_discussion', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        "gets the url needed to POST to delete the page"
        return reverse('delete_discussion', kwargs={'pk': self.pk})
    
    def get_lastpage_url(self):
        "gets the last page of the discussion"
        return "%s?page=%s" % (self.get_absolute_url(), self.pages)
    
    # USUALS
    def __unicode__(self):
        return self.title
