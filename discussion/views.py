from utils.shortcuts import context_response

from forms import *
from models import *

def search(request):
    # TODO: make solr
    pass

def view(request, pk):
    # view a discussion
    discussion = Discussion.objects.viewable(request.user).get_or_404(pk=pk)
    
    if request.GET.has_key('page'):
        discussion.page = request.page['page']
    
    return context_response(request, 'discussion/view.html', {
                'discussion': discussion,
            })


def edit(request, pk=None):
    discussion = Discussion.objects.editable(request.user).get_or_404(pk=pk) if pk else Discussion()
    
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