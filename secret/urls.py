from django.conf.urls.defaults import *
from contrib.views import delete
from models import *
from views import *

urlpatterns = patterns('',
    url(r'^secret/new/$', edit, name='new_secret'),
    url(r'^discussion/(?P<discussion_id>\d+)/secret/new/$', edit, {'from_discussion': True }, name='new_secret_for_discussion'),
    url(r'^secret/(?P<pk>\d+)/edit/$', edit, name='edit_secret'),
    url(r'^secret/(?P<pk>\d+)/delete/$', delete, {'model': Secret }, name='delete_secret'),
    url(r'^secret/(?P<pk>\d+)/', view, name='view_secret'),
)