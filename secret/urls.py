from django.conf.urls.defaults import *
from perm.views import delete
from models import *
from views import *

urlpatterns = patterns('',
    
    url(r'^secret/new/$', \
            edit, name='new_secret'),
    
    url(r'^secret/new_discussion/$', \
            edit, {'from_discussion': True }, name='new_secret_for_discussion'),
    
    url(r'^secret/(?P<pk>\d+)/edit/$', \
            edit, name='edit_secret'),
    
    url(r'^secret/(?P<pk>\d+)/delete/$', \
            delete, {'model': Secret }, name='delete_secret'),
    
    url(r'^secret/(?P<pk>\d+)_', \
            view, name='view_secret'),
    
    url(r'^secrets/$', \
            search, name='search_secrets'),
    
    url(r'^favourite_secret/(?P<secret_id>\d+)/add/$', \
            add_favourite_secret, name='create_favourite_secret'),
    
    url(r'^favourite_secret/(?P<secret_id>\d+)/delete/$', \
            delete_favourite_secret, name='delete_favourite_secret'),
)