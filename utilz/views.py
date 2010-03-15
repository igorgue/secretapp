from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from secret.models import Secret
from discussion.models import Discussion
from discussion.forms import DiscussionSearchForm
from secret.forms import SecretSearchForm
from comment.models import DiscussionComment, Proposal
from city.models import CITY_SESSION_NAME
from django.template.loader import render_to_string
from photo.models import UploadedPhoto
from shortcuts import context_response
import datetime
import random

def random_secret(request):
    " Redirects you to a random secret "
    return HttpResponseRedirect(Secret.viewable.order_by('?')[0].get_absolute_url())

def home(request):
    "Static page with links to all the city homes"
    return context_response(request, 'utilz/home.html', {}, tabs=['home'])

def city_home(request, city):
    " Landing page to site. Much more to come... "
    
    request.session[CITY_SESSION_NAME] = city
    request.session.modified = True
    
    START_DATE = datetime.datetime(*settings.START_DATE)
    NOW = datetime.datetime.now()    
    
    CURRENT_QUERY = ""
    CURRENT_SORT = "latest"
    CURRENT_PAGE = 1
    if request.GET:
        discussion_form = DiscussionSearchForm(request.GET)        
        secret_form = SecretSearchForm(request.GET)
        CURRENT_QUERY = request.GET.get('title', '')
        CURRENT_SORT = request.GET.get('usort', 'latest')
        CURRENT_PAGE = request.GET.get('page', 1)
    elif request.POST:
        discussion_form = DiscussionSearchForm(request.POST)
        secret_form = SecretSearchForm(request.POST)
        CURRENT_QUERY = request.POST.get('title', '')
        CURRENT_SORT = request.POST.get('usort', 'latest')
        CURRENT_PAGE = request.POST.get('page', 1)
    else:
        discussion_form = DiscussionSearchForm({'page':1})
        secret_form = SecretSearchForm({'page':1})

    d_ids = []
    discussion_results = None
    if discussion_form.is_valid():
        discussion_results = discussion_form.save()      
        for r in discussion_results.documents:
            d_ids.append(r.pk_field.value)
    
    #TODO sorting here
    discussions = Discussion.objects.filter(pk__in=d_ids).order_by("created_at")    
        
    s_ids = []
    secret_results = None
    if secret_form.is_valid():
        secret_results = secret_form.save()      
        for r in secret_results.documents:
            s_ids.append(r.pk_field.value)
    
    #TODO sorting here
    secrets = Secret.objects.filter(pk__in=s_ids).order_by("created_at")    
    
    show_large_search = True
    
    # TODO: cache this and randomize
    context = locals()
    
    if request.method == "POST":
        from django.utils import simplejson
        #build dict
        response_dict = {"discussions":"", "secrets":""}
        for discussion in discussions:
            response_dict['discussions'] += render_to_string('discussion/render/singular.html', { 'discussion': discussion })
        for secret in secrets:
            response_dict['secrets'] += render_to_string('secret/render/singular.html', { 'secret': secret })
        #wrap items in div with page number
        for k,d in response_dict.items():
            if d:
                response_dict[k] = "<div id='page%s' class='paged'>%s</div>" % (CURRENT_PAGE, d)
            
        return HttpResponse(simplejson.dumps(response_dict))
    else:
        return context_response(request, 'utilz/city_home.html', context, tabs=['home'])


def alt_home(request):
    START_DATE = datetime.datetime(*settings.START_DATE)
    NOW = datetime.datetime.now()
    
    # TODO: cache this and randomize
    context = {
        #'secrets': Secret.viewable.select_related().order_by('-created_at')[:20],
        'discussions': Discussion.viewable.select_related().order_by('-created_at')[:5],
        #'photos'
        'users': User.objects.order_by('-last_login')[:5],
        #'count' : {
        #    'users': User.objects.count(),
        #    'discussions': Discussion.viewable.count(),
        #    'secrets': Secret.viewable.count(),
        #    'posts': DiscussionComment.viewable.count(),
        #    'days': (NOW - START_DATE).days - 1,
        #}
    }
    return context_response(request, 'utilz/alt_home.html', context, tabs=['home'])
    


def render(request, template):
    " Displays any misc pages "
    try:
        return context_response(request, 'render/%s.html' % template, {}, tabs=['doc', template])
    except:
        raise Http404
    