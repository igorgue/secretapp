from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import settings

urlpatterns = patterns('',
    # internal
    (r'^', include('accounts.urls')),
    (r'^', include('comment.urls')),
    (r'^', include('perm.urls')),
    (r'^', include('discussion.urls')),
    (r'^', include('secret.urls')),
    
    # dependancies
    (r'^accounts/', include('socialauth.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    # contains landing page
    (r'^', include('utilz.urls')),
)

# loads all our standard template tags
from django import template
template.add_to_builtins('secretapp.utilz.templatetags.globals')

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
        #(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '%simages/favicon.ico' % settings.MEDIA_URL }),
    )
