from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from secret.models import Secret
from discussion.models import Discussion
from comment.models import DiscussionComment
from shortcuts import context_response


def random_secret(request):
    " Redirects you to a random secret "
    import random
    # TODO: cache this
    ids = Secret.viewable.values_list('id', flat=True)
    choice = random.choice(ids)
    return HttpResponseRedirect(Secret.objects.get(pk=choice).get_absolute_url())


def stats(request):
    " Redirects you to a random secret "
    context = {}
    try:
        context['discussion_count'] = Discussion.viewable.count()
        context['latest_discussion'] = Discussion.viewable.latest('created_at')
    except:
        pass
    try:
        context['secret_count'] =  Secret.viewable.count()
        context['latest_secret'] =  Secret.viewable.latest('created_at')
    except:
        pass
    try:
        context['comment_count'] =  DiscussionComment.viewable.count()
        context['latest_comment'] =  DiscussionComment.viewable.latest('created_at')
    except:
        pass
    try:
        context['user_count'] =  User.objects.count()
        context['latest_user'] =  User.objects.latest('pk')
    except:
        pass
    return context_response(request, 'utilz/stats.html', context)



def home(request):
    " Landing page to site. Much more to come... "
    # TODO: cache this and randomize
    context = {
        'secrets': Secret.viewable.all().order_by('-created_at'),
        'discussions': Discussion.viewable.all().order_by('-created_at'),
    }
    return context_response(request, 'utilz/home.html', context, tabs=['home'])


def render(request, template):
    " Displays any misc pages "
    try:
        return context_response(request, 'render/%s.html' % template, {}, tabs=['doc', template])
    except:
        raise Http404
    