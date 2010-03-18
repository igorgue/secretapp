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
    
    secrets = Secret.viewable.order_by("-created_at")[:5]
    discussions = Discussion.viewable.order_by("-updated_at")[:10]
    profiles = User.objects.order_by('-date_joined')[:5]
    photos = UploadedPhoto.objects.order_by("-created_at")[:6]
    
    return context_response(request, 'utilz/city_home.html', locals(), tabs=['home'])

def search(request, city):
    " Landing page to site. Much more to come... "
    
    request.session[CITY_SESSION_NAME] = city
    request.session.modified = True
    
    RESULTS_PER_PAGE = 10
    show_large_search = True
    START_DATE = datetime.datetime(*settings.START_DATE)
    NOW = datetime.datetime.now()    
    
    #determine if POST or GET and set dict for later use
    if request.GET:
        req_dict = request.GET
        CURRENT_TYPE = request.GET
    elif request.POST:
        req_dict = request.POST
    else:
        req_dict = {'page':1}
    
    CURRENT_QUERY = req_dict.get('text', '')
    CURRENT_SORT = req_dict.get('usort', 'latest')
    CURRENT_PAGE = int(req_dict.get('page', 1))
    CURRENT_TYPE = req_dict.get('type', 'secrets')
    CURRENT_LOCATION = req_dict.get('location','')
    NEXT_PAGE = CURRENT_PAGE + 1
    
    if CURRENT_TYPE == "discussions":
        discussion_form = DiscussionSearchForm(req_dict)
        RESULTS_PER_PAGE = discussion_form.Meta.results_per_page
        d_ids = []
        discussion_results = None
        if discussion_form.is_valid():
            discussion_results = discussion_form.save()      
            for r in discussion_results.documents:
                d_ids.append(r.pk_field.value)
        
        #TODO sorting here
        discussions = Discussion.objects.filter(pk__in=d_ids).order_by("created_at")
        num_results = 0
        rendered_results = ""
        for discussion in discussions:
            rendered_results += render_to_string('discussion/render/singular.html', { 'discussion': discussion, 'show_image': True })
            num_results += 1

    elif CURRENT_TYPE == "photos":
        secret_form = SecretSearchForm(req_dict)
        secret_form.chosen_template = "photo"
        RESULTS_PER_PAGE = secret_form.Meta.results_per_page
        s_ids = []
        secret_results = None
        if secret_form.is_valid():
            secret_results = secret_form.save()      
            for r in secret_results.documents:
                s_ids.append(r.pk_field.value)
        
        #TODO sorting here
        secrets = Secret.objects.filter(pk__in=s_ids).order_by("created_at")     
        num_results = 0
        rendered_results = ""
        for secret in secrets:
            rendered_results += render_to_string('secret/render/photo.html', { 'secret': secret })
            num_results += 1
    else:        
        secret_form = SecretSearchForm(req_dict)
        RESULTS_PER_PAGE = secret_form.Meta.results_per_page
        s_ids = []
        secret_results = None
        if secret_form.is_valid():
            secret_results = secret_form.save()      
            for r in secret_results.documents:
                s_ids.append(r.pk_field.value)
        
        #TODO sorting here
        secrets = Secret.objects.filter(pk__in=s_ids).order_by("created_at")     
        num_results = 0
        rendered_results = ""
        for secret in secrets:
            rendered_results += render_to_string('secret/render/singular.html', { 'secret': secret })
            num_results += 1
    
    if CURRENT_PAGE > 1:    
        rendered_results = "<div id='page%s' class='paged'>%s</div>" % (CURRENT_PAGE, rendered_results)
    
    HAS_MORE_RESULTS = (num_results == RESULTS_PER_PAGE) #if loaded full page's worth, then there could be more
    
    if request.method == "POST":
        from django.utils import simplejson
        
        response_dict = {"rendered_results":rendered_results, "num_results":num_results, "has_more_results":HAS_MORE_RESULTS}
        
        return HttpResponse(simplejson.dumps(response_dict))
    else:
        context = locals()
        return context_response(request, 'utilz/search.html', context, tabs=['home'])


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
    