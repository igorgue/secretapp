from django.conf.urls.defaults import *
from perm.views import delete
from models import *
from views import *

urlpatterns = patterns('',
    url(r'^discussion/new/$', edit, name='new_discussion'),
    url(r'^discussion/(?P<pk>\d+)/edit/$', edit, name='edit_discussion'),
    url(r'^discussion/(?P<pk>\d+)/delete/$', delete, {'model': Discussion }, name='delete_discussion'),
    url(r'^discussion/(?P<pk>\d+)/', view, name='view_discussion'),
)