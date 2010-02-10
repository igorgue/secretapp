from django.http import HttpResponseRedirect

from comment.forms import DiscussionCommentForm
from utils.shortcuts import context_response, get_editable_or_raise, get_viewable_or_raise

from forms import *
from models import *

def search(request):
    # TODO: make solr
    pass

def view(request, pk):
    # view a discussion
    discussion = get_viewable_or_raise(Discussion, request.user, pk=pk)
    
    if request.GET.has_key('page'):
        discussion.page = int(request.GET['page'])
    
    return context_response(request, 'discussion/view.html', {
                'discussion': discussion,
                'reply_form': DiscussionCommentForm().set_url(discussion),
            })


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
            })