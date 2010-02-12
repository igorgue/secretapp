from django.contrib.auth.models import User
from django.db import models

class UserSettings(models.Model):
    """
    Stores extra information about the user
    """
    user = models.ForeignKey(User)
    publish_to_wall = models.BooleanField(default=True)