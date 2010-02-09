from django.http import HttpResponseRedirect
from utils.shortcuts import context_response, get_editable_or_raise


def delete(request, pk, model):
    if request.method == 'POST':
        # get instance
        instance = get_editable_or_raise(model, request.user, pk=pk)
        # mark deleted
        instance.mark_deleted(request.user)
        # return
        if request.is_ajax():
            return context_response(request, 'ajax/deleted.html', {'instance': instance })

    return HttpResponseRedirect(request.META['HTTP_REFERER'])