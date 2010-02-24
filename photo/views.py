from utilz.shortcuts import context_response
from forms import *
from models import *


def upload(request, secret_id):
    """ """
    print "number of tests", TestPhoto.objects.count()
    
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(request, commit=True)
            instance.save()
            print instance
            print instance.image
            print form.cleaned_data['image']
            print instance.image.url

        print form.errors, form.non_field_errors()
    else:
        form = UploadPhotoForm()
    context = {
        'form': form
    }
    return context_response(request, 'photo/edit.html', context)