from django.core.urlresolvers import reverse
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
    
    def safe_title(self):
        from utils.manipulators import safe_title
        return safe_title(self.title)
    
    def get_asbolute_url(self):
        return "%s%s/" % (reverse('view_secret', kwargs={'pk':self.pk}), self.safe_title())
    
    def __unicode__(self):
        return self.title