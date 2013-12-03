# coding=utf-8

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
    url(r'^$', 'search.views.index', name='search-index'),
)
