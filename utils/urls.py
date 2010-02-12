from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^inspire/$', random_secret, name='random_secret'),
    url(r'^$', home, name='home'),
)