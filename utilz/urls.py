from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^inspire/$', random_secret, name='random_secret'),
    url(r'^$', home, name='splash'),
    url(r'^alt/$', alt_home, name='alt_home'),
    url(r'^doc/(?P<template>\w+)/$', render, name='render_template'),
    url(r'^(?P<city>\w+)/$', city_home, name='home'),
    url(r'^(?P<city>\w+)/search/$', search, name='search'),
)