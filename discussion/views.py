from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect

from comment.forms import DiscussionCommentForm
from utilz.shortcuts import context_response, get_editable_or_raise, get_viewable_or_raise, login_required

from forms import *
from models import *

def search(request):
    # if has been requested
    if request.GET:
        form = DiscussionSearchForm(request.GET)
    # otherwise default settings
    else:
        form = DiscussionSearchForm({'page': 1})
    
    # get the results
    if form.is_valid():
        results = form.save()
    else:
        results = []
    
    return context_response(request, 'discussion/search.html', {
                'search_form': form,
                'results': results,
            }, tabs=['discussions'])


def view(request, pk):
    # view a discussion
    discussion = get_viewable_or_raise(Discussion, request.user, pk=pk)
    
    # check seo
    seo_url = discussion.get_absolute_url() 
    if not request.get_full_path().split('?')[0] == seo_url:
        return HttpResponsePermanentRedirect(seo_url)
    
    # get page
    if request.GET.has_key('page'):
        discussion.page = int(request.GET['page'])
    
    return context_response(request, 'discussion/view.html', {
                'discussion': discussion,
                'reply_form': DiscussionCommentForm(permission_level=request.user.permission_level).set_url(discussion),
            }, tabs=['discussions'])


@login_required
def edit(request, pk=None):
    is_new = not pk
    discussion = get_editable_or_raise(Discussion, request.user, pk=pk) if pk else Discussion()
    
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion, permission_level=request.user.permission_level)
        if form.is_valid():
            discussion = form.save(request)
            if is_new:
                __send_mail(request, discussion)
            return HttpResponseRedirect(discussion.get_absolute_url())
    
    form = DiscussionForm(instance=discussion, permission_level=request.user.permission_level)
    return context_response(request, 'discussion/edit.html', {
                'form': form,
                'discussion': discussion,
            }, tabs=['discussions', 'edit'])


def __send_mail(request, discussion):
    "Send notification to a users on new discussion"
    from communication.models import CommunicationTrigger
    trigger = CommunicationTrigger.alive.get('new_discussion')
    trigger.create_communication( \
            request, request.user,
            # context to passed to templates
            {'discussion': discussion },
            # templates to be rendered
            subject_template='communication/new_discussion/subject.html',
            body_template='communication/new_discussion/body.html')

