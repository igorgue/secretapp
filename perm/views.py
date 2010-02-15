from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from utilz.shortcuts import context_response, get_editable_or_raise, login_required, redirect_back
from tools import *

@login_required
def reset_permissions(request):
    del request.session[PERMISSION_SESSION_NAME]
    request.session.modified = True
    return redirect_back(request)


@login_required
def delete(request, pk, model):
    if request.method == 'POST':
        # get instance
        instance = get_editable_or_raise(model, request.user, pk=pk)
        # mark deleted
        instance.mark_deleted(request.user)
        # return
        if request.is_ajax():
            return context_response(request, 'perm/ajax_deleted.html', {'instance': instance })
        else:
            return redirect_back(request)
    else:
        raise Http404