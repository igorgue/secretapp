from django.shortcuts import render_to_response
from django.template import RequestContext

def context_response(request, template, context, *args, **kwargs):
    """
    helper for
        http://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(template, context, *args, **kwargs)
