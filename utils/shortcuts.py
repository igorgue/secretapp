from django.shortcuts import render_to_response

def context_response(request, template, context, *args, **kwargs):
    """
    helper for
        http://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext
    """
    kwargs['context_instance'] = RequestContext(request)
    context, args, kwargs = handle_context_response(request, context, *args, **kwargs)
    return render_to_response(template, context, *args, **kwargs)
