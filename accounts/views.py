from django.contrib.auth.models import User
from django.contrib.auth import logout as ulogout
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404

from communication.forms import UserCommunicationSettingsForm
from utilz.shortcuts import context_response, redirect_back, login_required
from forms import *
from models import *


def facebook_login(request):
    """ Redirects you to home after facebook login """
    return redirect_back(request)

def fid_redirect(request, fid):
    """ Given a facebook fid, redirects to their profile page """
    user = get_object_or_404(User, username="FB:%s" % fid)
    return HttpResponseRedirect(user.get_absolute_url())


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


@login_required
def edit_communication(request):
    if request.method == 'POST':
        form = UserCommunicationSettingsForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect_back(request)
    else:
        form = UserCommunicationSettingsForm(user=request.user)
    return context_response(request, 'accounts/communication.html', 
                    {'form': form }, tabs=['profile', 'edit', 'communication'])


@login_required
def email_as_csv(request):
    # for superusers only
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')
    
    csv = ''
    for u in User.objects.all():
        if u.email:
            csv += '%s,%s,%s\n' % (u.email, u.first_name, u.last_name)
    response = HttpResponse(csv, mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=secret_london_email_list.csv'
    return response


@login_required
def logout(request):
    "logs a user out"
    ulogout(request)
    return redirect_back(request)

