from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^secret/(?P<secret_id>\d+)/upload_photo/$', \
            upload, name='upload_photo'),
)