from django import forms
from django.core.urlresolvers import reverse
from perm.forms import UserContentForm
from models import *


class SecretCommentForm(UserContentForm):
    text = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = SecretComment
        fields = ('text',)
        id = 'secretcomment'
    
    def set_url(self, secret, discussion=None, comment=None):
        if comment:
            self.action_url = reverse('edit_secret_comment', kwargs={'secret_id': secret.id, 'comment_id': comment.id })
        else:
            self.action_url = reverse('create_secret_comment', kwargs={'secret_id': secret.id })
        return self

class ProposalCommentForm(UserContentForm):
    text = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = ProposalComment
        fields = ('text',)
        use_form = True # this is so when creating multiple instances of the this form, urls are instance specific
    
    def set_url(self, proposal, comment=None):
        if comment:
            self.action_url = reverse('edit_proposal_comment', kwargs={'proposal_id': proposal.id, 'comment_id':comment.id })
        else:
            self.action_url = reverse('create_proposal_comment', kwargs={'proposal_id': proposal.id })
        return self


class DiscussionCommentForm(UserContentForm):
    secrets = forms.CharField(required=False, help_text="Comma seperated list of secret ids. e.g. 1,5,8,9 ")
    
    class Meta:
        model = DiscussionComment
        fields = ('text',)
    
    def set_url(self, discussion, comment=None):
        if comment:
            self.action_url = reverse('edit_discussion_comment', kwargs={'discussion_id': discussion.id, 'comment_id': comment.id })
        else:    
            self.action_url = reverse('create_discussion_comment', kwargs={'discussion_id': discussion.id })
        return self
    
    def save(self, request, discussion):
        instance = super(DiscussionCommentForm, self).save(request, commit=False)
        instance.discussion = discussion
        instance.save()
        lst = []
        for i in self.cleaned_data['secrets'].split(','):
            try:
                x = int(i)
            except:
                pass
            else:
                lst.append(x)
        secrets = Secret.viewable.filter(pk__in=lst)
        for s in secrets:
            p = Proposal()
            p.secret = s
            p.discussion_comment = instance
            p.save()
        return instance
