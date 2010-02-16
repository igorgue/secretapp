from django.contrib import admin
from django.http import HttpResponseRedirect

from bakery.models import UrlCache


class UrlCacheAdmin(admin.ModelAdmin):

    change_list_template = 'admin/url_cache/change_list.html'
    list_display = (
        'path', 'expire_after', 'was_updated', 'expires', 'current_value',
        'invalidate_now'
    )
    
    def changelist_view(self, request):
        # ?invalidate=PATH to invalidate the cache for something
        if 'invalidate' in request.GET:
            invalidate = request.GET['invalidate'];
            if invalidate == 'all':
                UrlCache.objects.all().update(value='')
            else: 
                UrlCache.objects.filter(path=invalidate).update(value = '')
            return HttpResponseRedirect(request.path)
        
        return super(UrlCacheAdmin, self).changelist_view(request)

admin.site.register(UrlCache, UrlCacheAdmin)
