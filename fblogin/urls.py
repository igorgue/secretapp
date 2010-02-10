from django.conf.urls.defaults import *
#from perm.views import delete
#from models import *
from views import *

urlpatterns = patterns('',
    url(r'^facebook/login/$', login),
)
