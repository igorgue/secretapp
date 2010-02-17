from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
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

@login_required
def flag_spam(request, modelid, objectid):
    msg = 'Thank you for letting us know about this post.'
    try:
        ct = ContentType.objects.get(pk = modelid)
        obj = ct.get_object_for_this_type(pk = objectid)
        obj.mark_spam(request.user)
    except IntegrityError:
        msg = 'You have already marked this item as being spam!'
    except:
        raise Http404

    return context_response(request, "perm/flag_spam.html", {'message': msg})
