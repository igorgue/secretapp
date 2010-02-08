from perm.models import UserContent
from django.db import models
from discussion.models import Discussion
from secret.models import Secret

class AbstractComment(UserContent):
    """ Helper abstract model. Pretty useless now. May add more later. """
    text = models.TextField()
    edit_permission = 'Keeper'
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.pk


class SecretComment(AbstractComment):
    """ A comment on a secret. Could be assosiciated with a discussion. """
    secret          = models.ForeignKey(Secret)
    discussion      = models.ForeignKey(Discussion, blank=True, null=True)

class DiscussionComment(AbstractComment):
    """ A comment on a discussion. Could have secrets associated with it. """
    discussion      = models.ForeignKey(Discussion)
    secrets         = models.ManyToManyField(Secret)