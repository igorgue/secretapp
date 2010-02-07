from contrib.shortcuts import context_response


def delete(request, pk, model):
    # get instance
    instance = model.objects.editable(request.user).get_or_404(pk=pk)
    # mark deleted
    instance.mark_deleted(request.user)
    # return
    if request.is_ajax():
        return context_response(request, 'ajax/deleted.html', {'instance': instance })
    else:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])