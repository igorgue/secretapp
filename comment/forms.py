from perm.forms import UserContentForm

def SecretCommentForm(UserContentForm):
    class Meta:
        model = SecretComment
        fields = ('text',)
    
    def set_url(secret, discussion=None):
        if discussion:
            self.Meta.url = reverse('create_discussion_secret_comment', \
                                    kwargs={'discussion_id': discussion.id, 'secret_id': secret.id })
        else:
            self.Meta.url = reverse('create_secret_comment', \
                                    kwargs={'secret_id': secret.id })


def DiscussionCommentForm(UserContentForm):
    secrets = forms.CharField(required=False)
    
    class Meta:
        model = DiscussionComment
        fields = ('text',)
    
    def set_url(discussion):
        self.Meta.url = reverse('create_discussion_comment', kwargs={'discussion_id': dicussion.id })
    
    def save(self, request):
        instance = super(DiscussionCommentForm, self).save(request)
        secrets = Secret.viewable.filter(pk__in=self.cleaned_data['secrets'])
        for s in secrets:
            instance.add(s)
        return instance