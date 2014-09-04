# coding=utf-8

from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView


urlpatterns = i18n_patterns('',
    url(r'^annotate/', 'annotate.views.index'),

    url(r'^browse/text/(?P<title>([^/])+)/(?P<juan>[0-9]+)$', 'browser.views.text_view_juan'),
    url(r'^browse/text/(?P<title>[^/]+)$', 'browser.views.text_view'),
    url(r'^browse/author/(?P<author>[A-Z])$', 'browser.views.index_author', {'startswith': True}),
    url(r'^browse/author/(?P<author>.*)$', 'browser.views.index_author', {'startswith': False}),
    url(r'^browse/', include('browser.urls', namespace='browse')),

    url(r'^r/(?P<title>([^/])+)/info$', 'r.views.text_info'),

    url(r'^sparql/(?P<lemma>.*)$', 'sparql.views.index'),

    url(r'^ocr/(?P<ocr_id>[0-9]+)$', 'ocr.views.show_processed'),
    url(r'^ocr/$', 'ocr.views.index'),

    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^wiki/', include('djiki.urls')),

    url(r'^documentation/',
        TemplateView.as_view(template_name='documentation/index.html')),

    url(r'^about/',
        TemplateView.as_view(template_name='about/index.html')),

    url(r'^$', 'roche.views.index'),
)
