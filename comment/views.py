from perm.shortcuts import context_response
from discussion.models import Discussion
from secret.models import Secret
from forms import *
from models import *

def create_secret_comment(request, secret_id):
    """ Comment directly on a Secret """
    secret = Secret.objects.viewable(request.user).get_or_404(pk=secret_id)
    
    if request.method == 'POST':
        form = SecretCommentForm(request.POST)
        if form.is_valid():
            # save instance data
            instance = form.save(request, commit=False)
            instance.secret = secret
            instance.save()
            
            # if successful
            if request.is_ajax():
                # return the rendered comment to be inserted
                return context_response(request, 'comment/secret.html', { 'instance': instance })
            else:
                # otherwise refresh the secret page
                return HttpResponseRedirect(instance.secret.get_absolute_url())
    else:
        form = SecretCommentForm()
    
    # sets the url for ajax
    form.set_url(secret)
    
    context = {
        'secret': secret,
        'form': form
    }
    if request.is_ajax():
        # is asked for by request and form rendered on failure
        return context_response(request, 'comment/ajax_secret.html', context)
    else:
        # should only see this on failure & with no js - crappy page though
        return context_response(request, 'comment/edit_secret.html', context)


def create_discussion_comment(request, discussion_id):
    """ Comment directly on a Discussion """
    discussion = Discussion.objects.viewable(request.user).get_or_404(pk=discussion_id)
    
    if request.method == 'POST':
        form = DiscussionCommentForm(request.POST)
        if form.is_valid():
            # see formModel for logic
            instance = form.save(request)
            
            # if successful just show discussion comment inline
            if request.is_ajax():
                return context_response(request, 'comment/discussion.html', { 'instance': instance })
            # otherwise go to last page of discussion
            else:
                return HttpResponseRedirect(instance.discussion.get_lastpage_url())
    else:
        form = DiscussionCommentForm()
    
    # sets the url for ajax
    form.set_url(discussion)
    
    context = { 'form': form }
    if request.is_ajax():
        return context_response(request, 'comment/ajax_discussion.html', context)
    else:
        return context_response(request, 'comment/edit_discussion.html', context)


def create_discussion_secret_comment(request, discussion_id, secret_id):
    """ Comment on a Secret on a Discussion """
    discussion = Discussion.objects.viewable(request.user).get_or_404(pk=discussion_id)
    secret = Secret.objects.viewable(request.user).get_or_404(pk=secret_id)
    
    if request.method == 'POST':
        form = SecretCommentForm(request.POST)
        if form.is_valid():
            # save the details
            instance = form.save(request, commit=False)
            instance.secret = secret
            instance.discussion = discussion
            instance.save()
            
            # if successful return comment as list inline
            if request.is_ajax():
                return context_response(request, 'comment/discussion_secret.html', { 'comment': instance })
            # otherwise return to the page of the discussion where the secret is mentioned
            else:
                return HttpResponseRedirect(instance.discussion.get_secretpage_url(secret))
    else:
        form = SecretCommentForm()
    
    # sets the url for ajax
    form.set_url(secret, discussion)
    discussion.set_page_by_secret(secret)
    
    context = {
        'form': form,
        'discussion': discussion,
        'secret': secret,
    }
    if request.is_ajax():
        # ajax form for discussion secret comment
        return context_response(request, 'comment/ajax_discussion_secret.html', context)
    else:
        # should only see this failure -- will open up on its own page
        return context_response(request, 'comment/edit_discussion_secret.html', context)


