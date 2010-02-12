from django.http import Http404
from utils.shortcuts import context_response
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
        if not user.active:
            raise Http404
    
    # augment with all the lovely cool data and functions
    return context_response(request, 'accounts/view.html', {
                'profile': augment_user(user),
                })


def edit(request):
    " Editing your profile "
    settings = request.user.settings
    successful = False
    
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            settings = form.save(commit=True)
            successful = True
            update_agument_session(request)
    else:
        form = UserSettingsForm(instance=settings)
    
    return context_response(request, 'accounts/edit.html', {
                'form': form,
                'successful': successful,
                })