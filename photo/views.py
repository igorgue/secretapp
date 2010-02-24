from secret.models import Secret
from utilz.shortcuts import context_response, get_editable_or_raise
from forms import *
from models import *


def upload(request, secret_id):
    """ Upload an image and attach it to a secret """
    secret = get_editable_or_raise(Secret, request.user, pk=secret_id)
    
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.secret = secret
            instance = form.save(request, commit=True)
    else:
        form = UploadPhotoForm()
    context = {
        'form': form
    }
    return context_response(request, 'photo/edit.html', context)