from django.contrib.auth import logout as ulogout
from django.http import Http404
from utilz.shortcuts import context_response, redirect_back
from tools import *
from forms import *
from models import *


def view(request, pk):
    " When viewing a User "
    
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


def edit(request):
    " Editing your profile "
    settings = request.user.get_settings()
    successful = False
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            settings = form.save(commit=True)
            successful = True
            update_agument_session(request)
    else:
        form = UserSettingsForm(instance=settings)
    
    return context_response(request, 'accounts/profile.html', {
                'profile': request.user,
                'form': form,
                'successful': successful,
            }, tabs=['profile', 'edit'])


def logout(request):
    "logs a user out"
    ulogout(request)
    return redirect_back(request)

