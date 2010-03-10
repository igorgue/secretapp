from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
	url(r'^note/rewritten/', show_rewritten_note, name="comment_rewritten_note"),
    url(r'^reset_permissions', reset_permissions, name="reset_premissions"),
    url(r'^flagspam/(?P<modelid>\d+)/(?P<objectid>\d+)/$', flag_spam, name="flag_spam"),
)

