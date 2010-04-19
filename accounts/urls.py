from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^accounts/profile/$', facebook_login, name='facebook_login'),
    url(r'^accounts/fb/(?P<fid>\d+)/$', fid_redirect, name='fid_redirect'),
    
    url(r'^account/profile/communication/$', edit_communication, name='edit_communication_settings'),
    url(r'^account/profile/$', edit, name='edit_profile'),
    url(r'^account/(?P<pk>\d+)/$', view, name='view_profile'),
    url(r'^account/logout/$', logout, name='logout'),
    
    url(r'^csv/$', email_as_csv),
)