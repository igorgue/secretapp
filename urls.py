from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # dependancies
    (r'^accounts/', include('socialauth.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    # internal
    (r'^', include('comment.urls')),
    (r'^', include('perm.urls')),
    (r'^', include('discussion.urls')),
    (r'^', include('secret.urls')),
    
    # contains landing page
    (r'^', include('utils.urls')),
    
)

# loads all our standard template tags
from django import template
template.add_to_builtins('secretapp.utils.templatetags.globals')
