from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^facebook/login/$', login, name="facebook_login"),
)
