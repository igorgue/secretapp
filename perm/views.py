from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from utilz.shortcuts import context_response, get_editable_or_raise, login_required, redirect_back
from tools import *


def show_rewritten_note(request):
	msg = """<p>In order to comply with Facebook's terms of use, we've had to re-write this posting in order to view it outside Facebook. If you aren't happy with this, when logged in you can change your postings back to what they were or delete them. If you're really, really not happy, then <a href="mailto:deletemystuffnow@secretlondon.us">email us</a> making sure to include a link to your Facebook profile page, and we'll be happy to delete all your stuff for good.</p>"""
	return context_response(request, "perm/generic_message.html", {'message': msg})	

@login_required
def reset_permissions(request):
    clear_permissions(request)
    return redirect_back(request)

@login_required
def delete(request, pk, model):
    if request.method == "POST":
        # get instance
        instance = get_editable_or_raise(model, request.user, pk=pk)
        # mark deleted
        instance.mark_deleted(request.user)
        # return
        if request.is_ajax():
            return context_response(request, 'perm/ajax_deleted.html', {'instance': instance })
        else:
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST['next'])
            else:
                return redirect_back(request)
    else:
        return Http404
        
@login_required
def flag_spam(request, modelid, objectid):
    msg = 'We have flagged this for review. Thank you for letting us know.'
    try:
        ct = ContentType.objects.get(pk = modelid)
        obj = ct.get_object_for_this_type(pk = objectid)
        obj.mark_spam(request.user)
    except IntegrityError:
        msg = 'You have already flagged this once. Thank you.'
    except:
        raise Http404

    return context_response(request, "perm/generic_message.html", {'message': msg})
