from contrib.shortcuts import context_response
from forms import *
from models import *

def search(request):
    # TODO: solr


def view(request, pk):
    return context_response(request, 'secret/view.html', {
                'secret': Secret.objects.viewable(request.user).get_or_404(pk=pk),
            })


def edit(request, pk, discussion=False):
    user = request.user
    # get object
    secret = Secret.objects.editable(user).get_or_404(pk=pk)
    
    if request.method == 'POST':
        form = SecretForm(request.POST, instance=secret)
        if form.is_valid():
            secret = form.save(request)
            # success and ajax
            if request.is_ajax():
                # if creating a secret as part of a discussion reply (need to return different template)
                if discussion:
                    return context_reponse(request, 'secret/snippets/comment.html', {'secret': secret })
                # otherwise creating it randomly somewhere else
                else:
                    return context_reponse(request, 'secret/snippets/list.html', {'secret': secret })
            # success redirect to instance page
            else:
                return HttpResponseRedirect(secret.get_absolute_url())
    else:
        form = SecretForm(instance=secret)
        
    # set the url
    form.set_url(secret)
    
    context = {
        'form': form,
        'secret': secret,
    }
    # is ajax creating / editing / failure
    if request.is_ajax():
        return context_response(request, 'secret/ajax.html', context)
    # otherwise
    else:
        return context_response(request, 'secret/edit.html', context)



