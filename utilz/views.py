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
from django.template import RequestContext
from django.template.loader import render_to_string
from photo.models import UploadedPhoto
from shortcuts import context_response
from utilz.shortcuts import login_required
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
    photos = UploadedPhoto.viewable.order_by("-created_at")[:10]
    
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
    CURRENT_SORT = req_dict.get('usort', 'relevance')
    CURRENT_PAGE = int(req_dict.get('page', 1))
    CURRENT_TYPE = req_dict.get('type', 'secrets')
    CURRENT_LOCATION = req_dict.get('location','')
    NEXT_PAGE = CURRENT_PAGE + 1
    
    if CURRENT_TYPE == "discussions":
        discussion_form = DiscussionSearchForm(req_dict)
        available_sorts = discussion_form.get_available_sort_orders()               
        num_results = 0
        rendered_results = ""
        if discussion_form.is_valid():
            discussion_results = discussion_form.save()      
            for r in discussion_results.documents:   
                discussion = Discussion.objects.get(pk=r.pk_field.value)
                discussion.title = r.fields['title'].highlighting()
                discussion.text = r.fields['text'].highlighting()
                discussion.highlighted_body = r.fields['blob'].highlighting()
                rendered_results += render_to_string('discussion/render/singular.html', { 'discussion': discussion, 'show_image': True }, RequestContext(request))
                num_results += 1
        
        RESULTS_PER_PAGE = discussion_form.Meta.results_per_page
        
    else:        
        secret_form = SecretSearchForm(req_dict)
        available_sorts = secret_form.get_available_sort_orders()
        template = 'secret/render/singular.html'
        if CURRENT_TYPE == "photos":
            secret_form.chosen_template = "photo"
            template = 'secret/render/photo.html'
            photo_browse = True
        num_results = 0
        rendered_results = ""
        if secret_form.is_valid():
            secret_results = secret_form.save()      
            for r in secret_results.documents:
                secret = Secret.objects.get(pk=r.pk_field.value)
                secret.title = r.fields['title'].highlighting()
                secret.location = r.fields['location'].highlighting()
                rendered_results += render_to_string(template, { 'secret': secret }, RequestContext(request))
                num_results += 1
        
        RESULTS_PER_PAGE = secret_form.Meta.results_per_page
    
    if CURRENT_PAGE > 1:    
        rendered_results = "<div id='page%s' class='paged'>%s</div>" % (CURRENT_PAGE, rendered_results)
    
    HAS_MORE_RESULTS = (num_results == RESULTS_PER_PAGE) #if loaded full page's worth, then there could be more
    
    if request.method == "POST":
        from django.utils import simplejson
        
        response_dict = {"rendered_results":rendered_results, "num_results":num_results, "has_more_results":HAS_MORE_RESULTS}
        
        return HttpResponse(simplejson.dumps(response_dict))
    else:
        return context_response(request, 'utilz/search.html', locals(), tabs=['home'])


@login_required
def alt_home(request):
    if not request.user.is_superuser or not request.user.is_staff:
        return HttpResponseRedirect("/")
    
    user_count = User.objects.count()
    user_with_email_count = User.objects.exclude(email="").count()
    secret_count = Secret.viewable.count()
    discussion_count = Discussion.viewable.count()
    post_count = DiscussionComment.viewable.count()
    photo_count = UploadedPhoto.viewable.count()
    
    return context_response(request, 'utilz/alt_home.html', locals(), tabs=['home'])
    


def render(request, template):
    " Displays any misc pages "
    return context_response(request, 'render/%s.html' % template, {}, tabs=['doc', template])
    try:
        pass
    except:
        raise Http404
    