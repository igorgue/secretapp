from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext


def context_response(request, template, context, *args, **kwargs):
    """
    helper for
        http://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(template, context, *args, **kwargs)


def get_object_or_404(Model, *args, **kwargs):
    "django version kills python... any ideas?"
    try:
        return Model.objects.get(*args, **kwargs)
    except Model.DoesNotExist:
        raise Http404


def get_editable_or_raise(Model, user, *args, **kwargs):
    """
    similar to 
        django.shortcuts.get_object_or_404
    but does permission check
    """
    if not isinstance(user, (User, AnonymousUser)):
        raise TypeError, "Please supply a user as the second argument"
    instance = get_object_or_404(Model, *args, **kwargs)
    if instance.is_editable(user):
        return instance
    else:
        raise PermissionDenied


def get_viewable_or_raise(Model, user, *args, **kwargs):
    """
    similar to above but does viewablility check
    """
    if not isinstance(user, (User, AnonymousUser)):
        raise TypeError, "Please supply a user as the second argument"
    instance = get_object_or_404(Model, *args, **kwargs)
    if instance.is_viewable(user):
        return instance
    else:
        raise Http404




