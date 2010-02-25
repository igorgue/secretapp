from django.contrib.auth.models import User
from django.contrib.auth import logout as ulogout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from socialauth.models import FacebookUserProfile

from utilz.shortcuts import context_response, redirect_back, login_required
from forms import *
from models import *


def view(request, pk):
    """ When viewing a User """
    # check permissions
    try:
        u = User.objects.get(pk=pk)
    except:
        raise Http404
    else:
        if not u.is_active:
            raise Http404
    
    # augment with all the lovely cool data and functions
    return context_response(request, 'accounts/profile.html', {
                'profile': u,
            }, tabs=['profile'])


def facebook_redirect(request, fid):
    """ Given a facebook fid, redirects to their profile page """
    fuser = get_object_or_404(FacebookUserProfile, facebook_uid=fid)
    return HttpResponseRedirect(fuser.user.get_absolute_url())


@login_required
def edit(request):
    " Editing your profile "
    conf = request.user.get_settings()
    successful = False
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST)
        if form.is_valid():
            form.user = request.user
            settings = form.save(commit=True)
            successful = True
    else:
        form = UserSettingsForm(initial={
            'email': request.user.email,
            'publish_to_wall': conf.publish_to_wall,
        })
    
    return context_response(request, 'accounts/profile.html', {
                'profile': request.user,
                'form': form,
                'successful': successful,
            }, tabs=['profile', 'edit'])


def logout(request):
    "logs a user out"
    ulogout(request)
    return redirect_back(request)

