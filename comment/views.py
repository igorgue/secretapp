from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from discussion.models import Discussion
from secret.models import Secret
from utilz.shortcuts import context_response, get_editable_or_raise, get_viewable_or_raise, redirect_back, select_related_object_or_404
from forms import *
from models import *

def create_secret_comment(request, secret_id):
    """ Comment directly on a Secret """
    secret = get_viewable_or_raise(Secret, request.user, pk=secret_id)
    
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
    discussion = get_viewable_or_raise(Discussion, request.user, pk=discussion_id)
    
    if request.method == 'POST':
        form = DiscussionCommentForm(request.POST)
        if form.is_valid():
            # see formModel for logic
            instance = form.save(request, discussion)
            
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


def create_proposal_comment(request, proposal_id):
    """ Comment on a Secret on a Discussion """
    proposal = select_related_object_or_404(Proposal, pk=proposal_id)
    
    if request.method == 'POST':
        form = ProposalCommentForm(request.POST)
        if form.is_valid():
            # save the details
            instance = form.save(request, commit=False)
            instance.proposal = proposal
            instance.save()
            
            # if successful return comment as list inline
            if request.is_ajax():
                return context_response(request, 'comment/proposal.html', { 'comment': instance })
            # otherwise return to the page of the discussion where the secret is mentioned
            else:
                return HttpResponseRedirect(proposal.discussion_comment.get_absolute_url())
    else:
        form = ProposalCommentForm()
    
    # sets the url for ajax
    form.set_url(proposal)
    
    context = {
        'form': form,
    }
    if request.is_ajax():
        # ajax form for discussion secret comment
        return context_response(request, 'comment/ajax_proposal.html', context)
    else:
        # should only see this failure -- will open up on its own page
        return context_response(request, 'comment/edit_proposal.html', context)


def agree_with_proposal(request, proposal_id):
    """ Clock up a favourite to a user... """
    if request.method == 'POST':
        props = get_object_or_404(Proposal, pk=proposal_id)
        # This creates a NEW entry even if this user previously created and then deleted
        # a favourite reference to a secret
        agree, new = Agreement.objects.get_or_create(proposal=props, created_by=request.user, deleted=False)
        
        if request.is_ajax():
            return HttpResponse('%s' % props.agreement_count)
        else:
            return redirect_back(request)
    else:
        raise Http404


