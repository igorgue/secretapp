import re
import random
import datetime

from django.http import HttpResponse
from django.conf import settings
from django.template import Template
from django.template.context import RequestContext

from bakery.models import UrlCache

REMOVE_COMMENTS = re.compile('<!--remove.*-->')


class UrlCacheMiddleware:
    """
    Simple URL Cache.
    
    Caches just 200's GET or HEAD requests and serves back
    that content from the cache
    
    Add to installed apps:
    
        INSTALLED_APPS += ('bakery',)
    
    And add the following middleware after vip_user is used:
        'bakery.middleware.UrlCacheMiddleware',
    
    To cache every url - simply add a cache row where the path=*
    
    If you want to dynamically opt out of using url cached data, then in the session
    set the path in the request.session['URL_CACHE_EXCEPTIONS'] list
    
    It is essential that pages which are cached in this way have any dynamic content
    that must ALWAYS be processed surround by {% noproc %} {% endnoproc %}
    
    Such dynamic content can only include user related items as no other data will
    be in the context.
    """
    
    def _second_pass(self, request, template):
        t = Template(template)
        render = t.render(RequestContext(request))
        return render
    
    def process_request(self, request):
        if (request.path.startswith('/admin/') or   
           request.path.startswith(settings.MEDIA_URL)):
            return None
        
        if not request.method in ('GET', 'HEAD'):
        # Only serve from cache on GET or HEAD requests
            request._url_cache_update_cache = False
            return None
        
        # Only serve if no query string
        if request.GET:
            return None

        # Check for any custom exceptions set in the sessions 
        url_cache_exceptions = getattr(request.session, 'URL_CACHE_EXCEPTIONS', [])
        if request.path in url_cache_exceptions:
            request._url_cache_update_cache = False
            return None
                
        # See if there is a cached item
        try:
            cached = UrlCache.objects.get(path=request.path)
        except UrlCache.DoesNotExist:
            # Normally, we only cache things that already exist in UrlCache!
            #
            # However, it is possible we are caching everything by adding a path = *
            # If so we will need to build the cache later on
            if not request.path.startswith('/admin/'):  
                try:
                    cache_everything = UrlCache.objects.get(path='*')
                    request._url_cache_update_cache = True
                except UrlCache.DoesNotExist:
                    # Remember, we only cache things that already exist in UrlCache
                    request._url_cache_update_cache = False
            
            return None
        
        # Has this cached page been populated and NOT expired?
        if not cached.is_usable():
            request._url_cache_update_cache = True
            return None
        
        # It's usable! Serve the request with it
        request._url_cache_used = True
        render = self._second_pass(request, cached.value)
        return HttpResponse(render, content_type = cached.content_type)

    def process_response(self, request, response):
        # store the un-cached version
        response_content = response.content
        if request.path.startswith('/admin') or request.path.startswith(settings.MEDIA_URL):        
            return response
        response.content = self._second_pass(request, response_content)
                
        # remove content between special tags
        response_content = REMOVE_COMMENTS.sub('', response_content)
        
        # Has process_request decided we need to update the cache?
        if not getattr(request, '_url_cache_update_cache', False):
            return response        

        # Only cache GET responses
        if request.method != 'GET':
            return response
            
        # Only cache 200s
        if not response.status_code == 200:
            return response
        
        # Only cache html
        if 'html' not in response['Content-Type']:
            return response
        
        # Update the cache we do a get or create incase we are making the cache on the fly
        url_cache, created = UrlCache.objects.get_or_create(path=request.path)
        # Update the object
        url_cache.value = response_content
        url_cache.content_type = response['Content-Type']
        url_cache.updated = datetime.datetime.now()
        url_cache.save()
        
        return response
