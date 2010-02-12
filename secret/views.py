from django.http import HttpResponseRedirect
from discussion.models import Discussion
from utils.shortcuts import context_response, get_editable_or_raise, get_viewable_or_raise, login_required
from forms import *
from secret.models import FavouriteSecret
from models import *
from django.http import Http404

def search(request):
    # TODO: make solr call
    template = request.GET.get('template', 'list')
    return context_response(request, 'secret/search.html', {
                'secrets': Secret.viewable.all(),
                'template': 'secret/render/%s.html' % template,
                'template_types': ('list', 'comment', 'photo'),
            })


def view(request, pk):
    return context_response(request, 'secret/view.html', {
                'secret': get_viewable_or_raise(Secret, request.user, pk=pk),
            })

@login_required
def edit(request, pk=None, discussion_id=None):
    user = request.user
    # get object
    secret = get_editable_or_raise(Secret, user, pk=pk) if pk else Secret()
    
    if request.method == 'POST':
        form = SecretForm(request.POST, instance=secret)
        if form.is_valid():
            secret = form.save(request)
            # success and ajax
            if request.is_ajax():
                # if creating a secret as part of a discussion reply (need to return different template)
                if discussion_id:
                    return context_reponse(request, 'secret/snippets/comment.html', {'secret': secret })
                # otherwise creating it randomly somewhere else
                else:
                    return context_reponse(request, 'secret/snippets/list.html', {'secret': secret })
            # success redirect to instance page
            else:
                # if creating as part of a discussion, redirect back to discussion
                if discussion_id:
                    # this is a serious failure if this happeneds - but try best to recover
                    return HttpResponseRedirect(reverse('view_discussion', kwargs={'pk': discussion_id }))
                # otherwise send to new page
                else:
                    return HttpResponseRedirect(secret.get_absolute_url())
    else:
        form = SecretForm(instance=secret)
        
    # set the urlG
    form.set_url(secret=secret, discussion=discussion_id)
    
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


def add_favourite_secret(request, secret_id):
    """ Clock up a favourite to a user... """
    if request.method == 'POST':
        secret = get_viewable_or_raise(Secret, request.user, pk=secret_id)
        # This creates a NEW entry even if this user previously created and then deleted
        # a favourite reference to a secret
        fave, new = FavouriteSecret.objects.get_or_create(secret=secret, created_by = request.user, deleted=False)
        
        if request.is_ajax():
            return context_response(request, 'ajax/new_favourite.html', {'instance': fave})
        if 'HTTP_REFERER' in request.META:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        raise Http404
        
def delete_favourite_secret(request, secret_id):
    """ Remove favourite from a user's list """
    if request.method == 'POST':
        # get instance
        secret = get_viewable_or_raise(Secret, request.user, pk=secret_id)
        # mark deleted on the only favourite flag that is set on this secret and has not
        # previously been deleted.
        fave = FavouriteSecret.objects.get(secret__id = secret.id, created_by = request.user, deleted=False)
        if fave.user_can_edit(request.user): 
            fave.mark_deleted(request.user)
        # return
        if request.is_ajax():
            return context_response(request, 'ajax/deleted.html', {'instance': fave })
        if 'HTTP_REFERER' in request.META:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        raise Http404

