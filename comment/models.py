from django.core.urlresolvers import reverse
from django.db import models

from perm.models import UserContent
from discussion.models import Discussion
from secret.models import Secret


class AbstractComment(UserContent):
    """ Helper abstract model. Pretty useless now. May add more later. """
    text = models.TextField()
    
    # see perm.models for details
    edit_permission = 'Keeper'
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return u"%s" % self.pk


class SecretComment(AbstractComment):
    """ A comment on a secret. Could be assosiciated with a discussion. """
    secret      = models.ForeignKey(Secret)

    def get_delete_url(self):
        return reverse('delete_secret_comment', kwargs={'pk': self.pk})


class DiscussionComment(AbstractComment):
    """ A comment on a discussion. Could have secrets associated with it. """
    discussion  = models.ForeignKey(Discussion)
    secrets     = models.ManyToManyField(Secret, through="Proposal")
    
    def viewable_secrets(self):
        return [p.secret for p in Proposal.viewable.filter(discussion_comment=self).select_related()]
    
    def get_delete_url(self):
        return reverse('delete_discussion_comment', kwargs={'pk': self.pk})


class ProposalManager(models.Manager):
    def get_query_set(self):
        return super(ProposalManager, self).get_query_set() \
            .filter(discussion_comment__deleted=False, \
                                secret__deleted=False)

class Proposal(models.Model):
    """ When you suggest a secret in a discussion """
    discussion_comment = models.ForeignKey(DiscussionComment)
    secret      = models.ForeignKey(Secret)
    
    viewable    = ProposalManager()
    objects     = models.Manager() 
    
    def get_agree_url():
        return reverse('agree_with_proposal', kwargs={'proposal_id':self.pk})
    
    def agreements(self):
        if not hasattr(self, '_agreements'):
            # TODO: cache this
            self._agreements = Agreement.viewable.filter(proposal=self).select_related()
        return self._agreements
    
    @property
    def agreement_count(self):
        if hasattr(self, '_agreements'):
            return len(self.agreements())
        else:
            if not hasattr(self, '_agreement_count'):
                self._agreement_count = Agreement.viewable.filter(proposal=self).count()
            return self._agreement_count


class ProposalComment(AbstractComment):
    """ A comment on a Proposal. """
    proposal        = models.ForeignKey(Proposal)

    def get_delete_url(self):
        return reverse('delete_proposal_comment', kwargs={'pk': self.pk})


class Agreement(UserContent):
    """ An endorsment on a secret proposal """
    proposal        = models.ForeignKey(Proposal)




