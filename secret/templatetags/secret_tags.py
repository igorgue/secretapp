"""
Tags for rendering comments on secrets
"""
from django import template
from django.template import escape
from django.utilz.safestring import SafeString

from secret.models import Secret

register = template.Library()

@register.inclusion_tag('secret/comments.html', takes_context = True)
def secret_comments(context, secret):
    comments = secret.secretcomment_set.all()
    comment_context ={ 'comments' : comments,
                      'count' : len(comments) 
                      }
    
    return comment_context
