import re
import random
import datetime

from django.http import HttpResponse
from django.conf import settings

from bakery.models import UrlCache

REMOVE_COMMENTS = re.compile('<!--remove.*-->')


class UrlCacheMiddleware:
    """
    Simple URL Cache.
    
    Caches just 200's GET or HEAD requests from anonymous users and serves back
    that content from the cache
    
    Add to installed apps:
    
        INSTALLED_APPS += ('bakery',)
    
    And add the following middleware after vip_user is used:
        'bakery.middleware.UrlCacheMiddleware',
    
    To cache every url - simply add a cache row where the path=*
    
    If you want to dynamically opt out of using url cached data, then in the session
    set the path in the request.session['URL_CACHE_EXCEPTIONS'] list
    """
    def process_request(self, request):
        # Only serve from cache on GET or HEAD requests with no query string
        if not request.method in ('GET', 'HEAD'):
            request._url_cache_update_cache = False
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
        return HttpResponse(cached.value, content_type = cached.content_type)

    def process_response(self, request, response):
                
        # Store the response content so we don't remove any ad placeholders in
        # the database
        response_content = response.content
        
        # Have we used the cache if so replace any ads holders
        if getattr(settings, 'ADS_RANDOM_PLACEHOLDER', False) and \
            settings.ADS_RANDOM_PLACEHOLDER in response.content:
            response.content = response.content.replace(
                settings.ADS_RANDOM_PLACEHOLDER,
                str(random.randint(99999, 999999))
            )
            
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
        
        # don't cache if we have a user
        if request.user.is_authenticated():
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
