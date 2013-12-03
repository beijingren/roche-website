# coding=utf-8

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
    #url(r'^text$', 'browser.views.text_view', name='text-view'),

    # index views
    #url(r'^author/(?P<author>[A-Z])$', 'browser.views.index_author', {'startswith': True}),
    #url(r'^author/(?P<author>.*)$', 'browser.views.index_author', {'startswith': False}),
    url(r'^title/(?P<letter>[A-Z])$', 'browser.views.index_title'),
    url(r'^$', 'browser.views.index', name='browser-index'),
)
