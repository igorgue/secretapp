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
                'newd_form': DiscussionForm().set_url(new=True),
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
                'reply_form': DiscussionCommentForm().set_url(discussion),
            }, tabs=['discussions'])


@login_required
def edit(request, pk=None):
    discussion = get_editable_or_raise(Discussion, request.user, pk=pk) if pk else Discussion()
    
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            discussion = form.save(request)
            return HttpResponseRedirect(discussion.get_absolute_url())
    
    form = DiscussionForm(instance=discussion)
    return context_response(request, 'discussion/edit.html', {
                'form': form,
                'discussion': discussion,
            }, tabs=['discussions', 'edit'])


