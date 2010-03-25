from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from discussion.models import Discussion
from secret.models import Secret
from utilz.shortcuts import context_response, get_editable_or_raise, get_viewable_or_raise, redirect_back, select_related_object_or_404
from utilz.manipulators import unique
from forms import *
from models import *

def create_secret_comment(request, secret_id, comment_id):
    """ Comment directly on a Secret """
    secret = get_viewable_or_raise(Secret, request.user, pk=secret_id)
    
    #if editing
    if comment_id:
        comment = get_editable_or_raise(SecretComment, request.user, pk=comment_id)
    
    if request.method == 'POST':
        if comment_id:
            form = SecretCommentForm(request.POST, instance=comment)
        else:
            form = SecretCommentForm(request.POST)
        if form.is_valid():
            # save instance data
            instance = form.save(request, commit=False)
            instance.secret = secret
            instance.save()
            # search save hook on secret
            secret.save()
            __secret_send_mail(request, secret, instance)
            # if successful
            if request.is_ajax():
                # return the rendered comment to be inserted
                return context_response(request, 'comment/secret.html', { 'instance': instance })
            else:
                # otherwise refresh the secret page
                return HttpResponseRedirect(instance.secret.get_absolute_url())
    else:
        if comment_id:
            form = SecretCommentForm(instance=comment)
        else:
            form = SecretCommentForm()
    
    # sets the url for ajax
    if comment_id:
        form.set_url(secret, comment)
    else:
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


def create_discussion_comment(request, discussion_id, comment_id=None):
    """ Comment directly on a Discussion """
    discussion = get_viewable_or_raise(Discussion, request.user, pk=discussion_id)
    
    #if editing
    if comment_id:
        comment = get_editable_or_raise(DiscussionComment, request.user, pk=comment_id)
    
    if request.method == 'POST':
        if comment_id:
            form = DiscussionCommentForm(request.POST, permission_level=request.user.permission_level, instance=comment)
        else:
            form = DiscussionCommentForm(request.POST, permission_level=request.user.permission_level)
        if form.is_valid():
            # see formModel for logic
            instance = form.save(request, discussion)
            # search save hook
            discussion.save()
            # sends mail once the comment is made
            __discussion_send_mail(request, discussion, instance)
            # if successful just show discussion comment inline
            if request.is_ajax():
                return HttpResponse('success')
            # otherwise go to last page of discussion
            else:
                return HttpResponseRedirect(instance.get_absolute_url())
    else:
        if comment_id:
            form = DiscussionCommentForm(permission_level=request.user.permission_level, instance=comment)
        else:
            form = DiscussionCommentForm(permission_level=request.user.permission_level)
    
    # sets the url for ajax
    if comment_id:
        form.set_url(discussion, comment)
    else:
        form.set_url(discussion)
    
    context = { 'form': form, 'discussion': discussion}
    if request.is_ajax():
        return context_response(request, 'comment/ajax_discussion.html', context)
    else:
        return context_response(request, 'comment/edit_discussion.html', context)


def create_proposal_comment(request, proposal_id, comment_id):
    """ Comment on a proposal """
    proposal = select_related_object_or_404(Proposal, pk=proposal_id)
    
    #if editing
    if comment_id:
        comment = get_editable_or_raise(ProposalComment, request.user, pk=comment_id)
    
    if request.method == 'POST':
        if comment_id:
            form = ProposalCommentForm(request.POST, permission_level=request.user.permission_level, instance=comment)
        else:
            form = ProposalCommentForm(request.POST, permission_level=request.user.permission_level)
        if form.is_valid():
            # save the details
            instance = form.save(request, commit=False)
            instance.proposal = proposal
            instance.save()
            # search save hooks
            proposal.secret.save()
            proposal.discussion_comment.discussion.save()
            
            # if successful return comment as list inline
            if request.is_ajax():
                return context_response(request, 'comment/proposal.html', { 'comment': instance })
            # otherwise return to the page of the discussion where the secret is mentioned
            else:
                return HttpResponseRedirect(proposal.discussion_comment.get_absolute_url())
    else:
        if comment_id:
            form = ProposalCommentForm(permission_level=request.user.permission_level, instance=comment)
        else:
            form = ProposalCommentForm(permission_level=request.user.permission_level)
    
    # sets the url for ajax
    if comment_id:
        form.set_url(proposal, comment)
    else:
        form.set_url(proposal)
    
    context = {
        'form': form,
        'proposal': proposal,
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
        if request.user.id == props.secret.created_by.id:
            if request.is_ajax():
                return HttpResponse('%s' % props.agreement_count)
            else:
                return redirect_back(request)
        # This creates a NEW entry even if this user previously created and then deleted
        # a favourite reference to a secret
        agree, new = Agreement.objects.get_or_create(proposal=props, created_by=request.user, deleted=False)
        
        if request.is_ajax():
            return HttpResponse('%s' % props.agreement_count)
        else:
            return HttpResponseRedirect(props.get_absolute_url())
    else:
        raise Http404


def __unique_contributors(items, contributor, creator):
    """ Gets a unique list of all the """
    contributors = dict([(c.created_by, None) for c in items])
    if contributor in contributors:
        del contributors[contributor]
    if creator in contributors:
        del contributors[creator]
    return unique(contributors.keys())


def __discussion_send_mail(request, discussion, action_item):
    "sends notification when someone comments on a discussion"
    from communication.models import CommunicationTrigger
    context = {'discussion': discussion, 'action_item': action_item }
    # send message to discussion creator
    trigger = CommunicationTrigger.alive.get(name='replied_discussion_creator')
    trigger.create_communication(request,
            discussion.created_by, context,
            subject_template='communication/replied_discussion/creator/subject.txt',
            body_template='communication/replied_discussion/creator/body.txt')
    # send messages to contributors (unique by user)
    trigger = CommunicationTrigger.alive.get(name='replied_discussion_contributor')
    contributors = __unique_contributors(discussion.comments(), request.user, discussion.created_by)
    for contributor in contributors:
        trigger.create_communication(request,
                contributor, context,
                subject_template='communication/replied_discussion/contributor/subject.txt',
                body_template='communication/replied_discussion/contributor/body.txt')


def __secret_send_mail(request, secret, action_item, action=None):
    "sends notification when someone comments on a secret"
    # this is also used in secret_photographed
    if not action:
        action = 'secret_commented'
    
    from communication.models import CommunicationTrigger
    trigger = CommunicationTrigger.alive.get(name='replied_secret_creator')
    context = {'secret': secret, 'action_item': action_item }
    user = request.user
    creator = secret.created_by
    
    # send message to secret creator
    trigger.create_communication(request,
            creator, context,
            subject_template='communication/%s/creator/subject.txt' % action,
            body_template='communication/%s/creator/body.txt' % action)
    
    # send message to contributors
    trigger = CommunicationTrigger.alive.get(name='replied_secret_creator')
    
    # send message to commentators, photographers
    for items, name in ((secret.comments(), 'commentor'), (secret.photos(), 'photographer')):
        contributors = __unique_contributors(items, user, creator)
        for contributor in contributors:
            trigger.create_communication(request,
                contributor, context,
                subject_template='communication/%s/%s/subject.txt' % (action, name),
                body_template='communication/%s/%s/body.txt' % (action, name))
    
