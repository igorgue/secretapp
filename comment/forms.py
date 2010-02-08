from contrib.forms import UserContentForm

def SecretCommentForm(UserContentForm):
    class Meta:
        model = SecretComment
        fields = ('text',)
    
    def set_url(secret, discussion=None):
        if discussion:
            self.Meta.url = reverse('create_discussion_secret_comment', \
                                    {'discussion_id': discussion.id, 'secret_id': secret.id })
        else:
            self.Meta.url = reverse('create_secret_comment', \
                                    {'secret_id': secret.id })


def DiscussionCommentForm(UserContentForm):
    secrets = forms.CharField(required=False)
    
    class Meta:
        model = DiscussionComment
        fields = ('text',)
    
    def set_url(discussion):
        self.Meta.url = reverse('create_discussion_comment', {'discussion_id': dicussion.id })
    
    def save(self, request):
        instance = super(DiscussionCommentForm, self).save(request)
        secrets = Secret.objects.viewable(request.user).filter(pk__in=self.cleaned_data['secrets'])
        for s in secrets:
            instance.add(s)
        return instance