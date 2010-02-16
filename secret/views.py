from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, QueryDict
from django.shortcuts import get_object_or_404
from discussion.models import Discussion
from comment.forms import SecretCommentForm
from secret.forms import SecretSearchForm
from utilz.shortcuts import context_response, get_editable_or_raise, get_viewable_or_raise, login_required, redirect_back
from forms import *
from models import *


def search(request):
    # if has been requested
    if request.GET:
        form = SecretSearchForm(request.GET)
    # otherwise default settings
    else:
        form = SecretSearchForm({'page': 1})
    
    if request.is_ajax():
        form.Meta.default_template = 'location'
    
    # 
    template_map_numbers = {
        'location': 50,
        'list': 10,
        'photo': 20,
    }
    
    # get the results
    if form.is_valid():
        if form.cleaned_data.get('template') and form.cleaned_data['template']:
            form.Meta.results_per_page = template_map_numbers[form.cleaned_data['template']]
        results = form.save()
    else:
        results = []
    
    search_template = 'secret/layout/%s.html' % form.render_template()
    if request.is_ajax():
        render_template = search_template
    else:
        render_template = 'secret/search.html'
    
    # return
    return context_response(request, render_template, {
                'form': form,
                'results': results,
                'search_template':  search_template,
                # this will be hard coded into tabs
                'template_types': SECRET_RENDER_TEMPLATES,
            }, tabs=['secrets', form.render_template()])


def view(request, pk):
    # get secret
    secret = get_viewable_or_raise(Secret, request.user, pk=pk)
    # check url for seo
    seo_url = secret.get_absolute_url()
    if not request.get_full_path().split('?')[0] == seo_url:
        return HttpResponsePermanentRedirect(seo_url)
    return context_response(request, 'secret/view.html', {
                'secret': secret,
                'comment_form': SecretCommentForm().set_url(secret),
            }, tabs=['secrets'])


@login_required
def edit(request, pk=None, from_discussion=False):

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
                if from_discussion:
                    return HttpResponse('%s' % secret.pk if hasattr(secret, 'pk') and secret.pk else '')
                # otherwise creating it randomly somewhere else
                else:
                    return context_response(request, 'secret/render/list.html', {'secret': secret })
            # success redirect to instance page
            else:
                # if creating as part of a discussion, redirect back to discussion
                if from_discussion:
                    # this is a serious failure if this happeneds - but try best to recover
                    return HttpResponseRedirect(reverse('new_secret'))
                # otherwise send to new page
                else:
                    return HttpResponseRedirect(secret.get_absolute_url())
    else:
        form = SecretForm(instance=secret)
        
    # set the urlG
    form.set_url(secret=secret)
    
    
    context = {
        'form': form,
        'secret': secret,
    }
    if request.is_ajax():
        return HttpResponse('')
    else:
        return context_response(request, 'secret/edit.html', context, tabs=['secrets', 'edit'])


def add_favourite_secret(request, secret_id):
    """ Clock up a favourite to a user... """
    if request.method == 'POST':
        secret = get_viewable_or_raise(Secret, request.user, pk=secret_id)
        # This creates a NEW entry even if this user previously created and then deleted
        # a favourite reference to a secret
        fave, new = FavouriteSecret.objects.get_or_create(secret=secret, created_by=request.user, deleted=False)

        if request.is_ajax():
            return HttpResponse('%s' % secret.favourite_count)
        else:
            return redirect_back(request)
    else:
        raise Http404


def delete_favourite_secret(request, secret_id):
    """ Remove favourite from a user's list """
    if request.method == 'POST':
        # get instance
        secret = get_viewable_or_raise(Secret, request.user, pk=secret_id)
        # mark deleted on the only favourite flag that is set on this secret and has not
        # previously been deleted.
        fave = get_object_or_404(FavouriteSecret, secret=secret, created_by=request.user, deleted=False)
        if fave.user_can_edit(request.user): 
            fave.mark_deleted(request.user)
        # return
        if request.is_ajax():
            return context_response(request, 'perm/ajax_deleted.html', {'instance': fave })
        else:
            return redirect_back(request)
    else:
        raise Http404



