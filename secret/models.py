from django.db import models
from django.utils.translation import ugettext_lazy as _
from perm.models import UserContent

class Secret(UserContent):
    """
    The social object of secretapp
    """
    title           = models.CharField(max_length=250)
    description     = models.TextField(blank=True, null=True)
    location        = models.CharField(max_length=250, blank=True, null=True)
    latitude        = models.FloatField(blank=True, null=True)
    longitude       = models.FloatField(blank=True, null=True)
    google_reff     = models.CharField(max_length=250, blank=True, null=True)
    url             = models.URLField(blank=True, null=True)
    
    edit_permission = 'Keeper'
    
    
    # URLS
    def seo_string(self):
        from utilz.manipulators import safe_title
        return safe_title("%s %s" % (self.title, self.location if self.location else ''))
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return "%s%s/" % (reverse('view_secret', kwargs={'pk':self.pk}), self.seo_string())
    
    def get_edit_url(self):
        from django.core.urlresolvers import reverse
        return reverse('edit_secret', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        from django.core.urlresolvers import reverse
        return reverse('delete_secret', kwargs={'pk': self.pk})
    
    # IMAGES
    def primary_photo(self):
        from photo.models import UploadedPhoto
        try:
            return UploadedPhoto.viewable.filter(secret=self).order_by('created_at')[0]
        except:
            return None
    
    def photos(self):
        from photo.models import UploadedPhoto
        return UploadedPhoto.viewable.filter(secret=self).select_related()
    
    # COMMENTS
    def comments(self):
        if not hasattr(self, '_comments'):
            from comment.models import SecretComment
            self._favourites = SecretComment.viewable.filter(secret=self).select_related()
        return self._favourites
    
    @property
    def comment_count(self):
        from comment.models import SecretComment
        return SecretComment.viewable.filter(secret=self).count()
    
    # PROPOSALS
    def proposals(self):
        if not hasattr(self, '_proposals'):
            from comment.models import Proposal
            self._proposals = Proposal.viewable.filter(secret=self).select_related()
        return self._proposals
    
    @property
    def proposal_count(self):
        from comment.models import Proposal
        return Proposal.viewable.filter(secret=self).count()    
    
    # FAVOURITES (BEEN THERE)
    def favourites(self):
        if not hasattr(self, '_favourites'):
            self._favourites = FavouriteSecret.viewable.filter(secret=self).select_related()
        return self._favourites
    
    @property
    def favourite_count(self):
        return FavouriteSecret.viewable.filter(secret=self).count()
    
    # USUALS
    def __unicode__(self):
        return self.title


class FavouriteSecret(UserContent):
    """ This is now BEEN THERE! model """
    secret          = models.ForeignKey(Secret)
    
    def get_delete_url(self):
        return reverse('delete_favourite_secret', kwargs={'secret_id': self.secret.pk})


