from django.conf.urls.defaults import *
from contrib.views import delete
from views import *

urlpatterns = patterns('',
    # create comments
    url(r'^secret/(?P<secret_id>\d+)/comment/', \
            create_secret_comment, name='create_secret_comment'),
    
    url(r'^discussion/(?P<discussion_id>\d+)/comment/', \
            create_discussion_comment, name='create_discussion_comment'),
    
    url(r'^discussion_secret/(?P<discussion_id>\d+)/(?P<secret_id>\d+)/comment/', \
            create_discussion_secret_comment, name='create_discussion_secret_comment'),
    
    # delete comments
    url(r'^secret_comment/(?P<pk>\d+)/delete/$', \
            delete, {'model': SecretComment }, name='delete_secret_comment'),
    
    url(r'^discussion_comment/(?P<pk>\d+)/delete/$', \
            delete, {'model': DiscussionComment }, name='delete_discussion_comment'),
)

