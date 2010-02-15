from django.db import models
from django.utils.translation import ugettext_lazy as _
from perm.models import UserContent

class Secret(UserContent):
    """
    The social object of secretapp
    """
    title           = models.CharField(help_text=_("Name of secret"), max_length=250)
    description     = models.TextField(help_text=_("Description of secret. Will become wiki later."), blank=True, null=True)
    location        = models.CharField(help_text=_("Human readable location of secret"), max_length=250, blank=True, null=True)
    latitude        = models.FloatField(blank=True, null=True)
    longitude       = models.FloatField(blank=True, null=True)
    google_reff     = models.CharField(max_length=250, blank=True, null=True)
    url             = models.URLField(blank=True, null=True)
    
    edit_permission = 'Keeper'
    
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
    
    def favourites(self):
        if not hasattr(self, '_favourites'):
            self._proposals = FavouriteSecret.viewable.filter(secret=self).select_related()
        return self._proposals
    
    @property
    def favourite_count(self):
        if hasattr(self, '_favourites'):
            return len(self.favourites())
        else:
            if not hasattr(self, '_favourite_count'):
                self._favourite_count = FavouriteSecret.viewable.filter(secret=self).count()
            return self._favourite_count
    
    def __unicode__(self):
        return self.title


class FavouriteSecret(UserContent):
    """ A Reference to a secret rated as favourite for a person. """
    secret          = models.ForeignKey(Secret)
    
    def get_delete_url(self):
        return reverse('delete_favourite_secret', kwargs={'secret_id': self.secret.pk})


