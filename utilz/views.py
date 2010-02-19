from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from secret.models import Secret
from discussion.models import Discussion
from discussion.forms import DiscussionSearchForm, SORT_ORDERS as DISCUSSION_SORT_ORDERS
from comment.models import DiscussionComment, Proposal
from shortcuts import context_response
import datetime
import random

def random_secret(request):
    " Redirects you to a random secret "
    return HttpResponseRedirect(Secret.viewable.order_by('?')[0].get_absolute_url())


def home(request):
    " Landing page to site. Much more to come... "
    START_DATE = datetime.datetime(*settings.START_DATE)
    NOW = datetime.datetime.now()
    
    # TODO: cache this and randomize
    context = {
        'secrets': Secret.viewable.select_related().order_by('-created_at')[:3],
        'discussions': Discussion.viewable.select_related().order_by('-created_at')[:6],
        #'photos'
        'users': User.objects.order_by('-last_login')[:4],
        'count' : {
            'users': User.objects.count(),
            'discussions': Discussion.viewable.count(),
            'secrets': Secret.viewable.count(),
            'posts': DiscussionComment.viewable.count(),
            'days': (NOW - START_DATE).days - 1,
        }
    }
    return context_response(request, 'utilz/home.html', context, tabs=['home'])


def alt_home(request):
    START_DATE = datetime.datetime(*settings.START_DATE)
    NOW = datetime.datetime.now()
    
    # TODO: cache this and randomize
    context = {
        'secrets': Secret.viewable.select_related().order_by('-created_at')[:20],
        'discussions': Discussion.viewable.select_related().order_by('-created_at')[:30],
        #'photos'
        'users': User.objects.order_by('-last_login')[:20],
        'count' : {
            'users': User.objects.count(),
            'discussions': Discussion.viewable.count(),
            'secrets': Secret.viewable.count(),
            'posts': DiscussionComment.viewable.count(),
            'days': (NOW - START_DATE).days - 1,
        }
    }
    return context_response(request, 'utilz/alt_home.html', context, tabs=['home'])
    


def render(request, template):
    " Displays any misc pages "
    try:
        return context_response(request, 'render/%s.html' % template, {}, tabs=['doc', template])
    except:
        raise Http404
    