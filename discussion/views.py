from contrib.shortcuts import context_response

from forms import *
from models import *

def search(request):
    # TODO: make solr


def view(request, pk):
    # view a discussion
    discussion = Discussion.objects.viewable(request.user).get_or_404(pk=pk)
    
    #TODO: work out page stuff
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
    else:
        form = DiscussionForm(instance=discussion)
        return context_response(request, 'discussion/edit.html', {
                    'discussion': discussion,
                })