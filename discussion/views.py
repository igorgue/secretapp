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
    
    d_ids = []
    for r in results.documents:
        d_ids.append(r.pk_field.value)
    
    #TODO sorting here
    discussions = Discussion.objects.filter(pk__in=d_ids).order_by("-created_at")
    
    return context_response(request, 'discussion/search.html', {
                'search_form': form,
                'discussions': discussions,
                'results': results,
            }, tabs=['discussions'])


def view(request, pk):
    # view a discussion
    discussion = get_viewable_or_raise(Discussion, request.user, pk=pk)
    
    form = DiscussionCommentForm()
    
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
    discussion = get_editable_or_raise(Discussion, request.user, pk=pk) if pk else Discussion()
        
    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion, permission_level=request.user.permission_level)
        if form.is_valid():
            discussion = form.save(request)
            extra = "?fb=d" if not pk else ""
            return HttpResponseRedirect(discussion.get_absolute_url() + extra)
    
    form = DiscussionForm(instance=discussion, permission_level=request.user.permission_level)
    return context_response(request, 'discussion/edit.html', {
                'form': form,
                'discussion': discussion,
            }, tabs=['discussions', 'edit'])

