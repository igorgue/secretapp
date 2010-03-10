from django.http import HttpResponseRedirect
from secret.models import Secret
from utilz.shortcuts import context_response, get_editable_or_raise, login_required
from forms import *
from models import *

@login_required
def upload(request, secret_id):
    """ Upload an image and attach it to a secret """
    secret = get_editable_or_raise(Secret, request.user, pk=secret_id)
    
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.secret = secret
            instance = form.save(request, commit=True)
            from comment.views import __secret_send_mail
            __secret_send_mail(request, secret, instance, action='secret_photographed')
            return HttpResponseRedirect(secret.get_absolute_url()+"?fb=p")
    else:
        form = UploadPhotoForm()
    context = {
        'form': form
    }
    return context_response(request, 'photo/edit.html', context, tabs=['secret','photo'])