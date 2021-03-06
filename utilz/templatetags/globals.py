from django import template
from django.utils.translation import ugettext as _
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.inclusion_tag('templatetags/forms/form.html')
def form(form, id=None):
    """
    Shortcut to initialize a standard form.
    Implements Meta data stored on form instance, applies in forms.py
    
    Template Usage:
        {% form form %}
    
    Example form use:
        class Meta:
            url = 'some/url/to/'
            method = 'GET'
    """
    return { 'form': form, 'id': id }


@register.inclusion_tag('templatetags/forms/field.html')
def field(field, classes=None):
    """
    Shortcut for using a standard field
    
    Template Usage:
        {% field form.title 'left short' %}
    
    The 'left short' are classes which you want to apply to
    the containing div class
    """
    return { 'field': field, 'classes': classes }


@register.inclusion_tag('templatetags/forms/endform.html')
def endform(text=_('Submit'), classes=None):
    """
    Shortcut to close a form
    
    Template Usage:
        {% endform _('Go') 'right small' %}
    
    The 'right small' are classes which you want to apply to
    the containing div class
    
    The _('Go') is the translated action word you
    want to appear in the button
    """
    return { 'text': text, 'classes': classes }

@register.simple_tag
def call(obj, func_name, args):
    """
    Calls any given function with the params provided.
    WARN: This is an ugly function. Be careful when asking for this!
    
    Template Usage:
        {% call object "small" %}
    """
    return getattr(obj, func_name)(args)

@register.filter
@stringfilter
def urlizenf(text):
    """
    Same as urlize except it transforms the links to have rel="nofollow"
        >>> www.someurl.com
        <a href="http://www.someurl.com" rel="nofollow">www.someurl.com</a>
    """
    from django.utils.html import urlize
    return urlize(text, None, True, True)




