from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^inspire/$', random_secret, name='random_secret'),
    url(r'^stats/$', stats, name='stats'),
    url(r'^$', home, name='home'),
    url(r'^flagspam/(?P<modelid>\d+)/(?P<objectid>\d+)/$', flag_spam),
    url(r'^(?P<template>\w+)/$', render, name='render_template'),
)