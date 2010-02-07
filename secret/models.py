from django.db import models
from django.utils.translation import ugettext_lazy as _
from contrib.models import UserContent

class Secret(UserContent):
    """
    The social object of secretapp
    """
    title           = models.CharField(help_text=_("Name of secret"), max_length=250)
    description     = models.TextField(help_text=_("Description of secret. Will become wiki later."))
    location        = models.CharField(help_text=_("Human readable location of secret"), max_length=250)
    latitude        = models.FloatField()
    longitude       = models.FloatField()
    google_reff     = models.CharField(max_length=250)
    url             = models.URLField(blank=True, null=True)
    