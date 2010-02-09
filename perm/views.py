from utils.shortcuts import context_response


def delete(request, pk, model):
    if request.method == 'POST':
        # get instance
        instance = model.objects.editable(request.user).get_or_404(pk=pk)
        # mark deleted
        instance.mark_deleted(request.user)
        # return
        if request.is_ajax():
            return context_response(request, 'ajax/deleted.html', {'instance': instance })

    return HttpResponseRedirect(request.META['HTTP_REFERER'])