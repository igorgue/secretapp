from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from utils.shortcuts import context_response, get_editable_or_raise, login_required

@login_required
def delete(request, pk, model):
    if request.method == 'POST':
        # get instance
        instance = get_editable_or_raise(model, request.user, pk=pk)
        # mark deleted
        instance.mark_deleted(request.user)
        # return
        if request.is_ajax():
            return context_response(request, 'ajax/deleted.html', {'instance': instance })
        if 'HTTP_REFERER' in request.META:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        raise Http404