from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('comment.urls')),
    (r'^', include('perm.urls')),
    (r'^', include('discussion.urls')),
    (r'^', include('secret.urls')),
    
    # contains landing page
    (r'^', include('utils.urls')),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)