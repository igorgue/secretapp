from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, QueryDict
from discussion.models import Discussion
from secret.forms import SecretSearchForm
from utilz.shortcuts import context_response, get_editable_or_raise, get_viewable_or_raise, login_required
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
        form.Meta.results_per_page = 500
        form.Meta.default_template = 'location'
    
    # get the results
    if form.is_valid():
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
            })


def view(request, pk):
    # get secret
    secret = get_viewable_or_raise(Secret, request.user, pk=pk)
    # check url for seo
    seo_url = secret.get_absolute_url()
    if not request.get_full_path().split('?')[0] == seo_url:
        return HttpResponsePermanentRedirect(seo_url)
    return context_response(request, 'secret/view.html', {
                'secret': secret,
            })


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
                    return HttpResponse('%s' % secret if hasattr(secret, 'pk') and secret.pk else '')
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
        return context_response(request, 'secret/edit.html', context)



