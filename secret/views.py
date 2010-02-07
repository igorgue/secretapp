from contrib.shortcuts import context_response
from forms import *
from models import *

def search(request):
    # TODO: solr

def view(request, pk):
    return context_response(request, 'secret/view.html', {
                'secret': Secret.objects.viewable(request.user).get_or_404(pk=pk),
            })


def edit(request, pk):
    user = request.user
    # get object
    secret = Secret.objects.editable(user).get_or_404(pk=pk)
    
    if request.method == 'POST':
        form = SecretForm(request.POST, instance=secret)
        if form.is_valid():
            secret = form.save(request)
            # success and ajax
            if request.is_ajax():
                return context_reponse(request, 'secret/ajax_success.html', {'secret': secret })
            # success redirect to instance page
            else:
                return HttpResponseRedirect(secret.get_absolute_url())
    else:
        form = SecretForm(instance=secret)
        
        context = {'secret': secret }
        # is ajax creating / editing / failure
        if request.is_ajax():
            return context_response(request, 'secret/snippets/list.html', context)
        # otherwise
        else:
            return context_response(request, 'secret/edit.html', context)

