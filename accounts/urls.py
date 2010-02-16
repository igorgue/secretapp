from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^accounts/profile/$', edit, name='edit_profile'),
    url(r'^accounts/(?P<pk>\d+)/$', view, name='view_profile'),
    url(r'^accounts/logout/$', logout, name='logout'),
)