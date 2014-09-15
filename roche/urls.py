# coding=utf-8

from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

from django.contrib import admin

urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^annotate/uima/(?P<uima_id>[0-9]+)$', 'annotate.views.show_annotated'),
    url(r'^annotate/uima/', 'annotate.views.index'),
    url(r'^annotate/(?P<function>.*)/(?P<lemma>.*)$', 'annotate.views.annotate'),

    url(r'^browse/text/(?P<title>([^/])+)/(?P<juan>[0-9]+)$', 'browser.views.text_view_juan'),
    url(r'^browse/text/(?P<title>([^/])+)/(?P<juan>[0-9]+)/(?P<file_format>(txt|pdf))$', 'r.views.text_download'),
    url(r'^browse/text/(?P<title>[^/]+)$', 'browser.views.text_view'),
    url(r'^browse/author/(?P<author>[A-Z])$', 'browser.views.index_author', {'startswith': True}),
    url(r'^browse/author/(?P<author>.*)$', 'browser.views.index_author', {'startswith': False}),
    url(r'^browse/', include('browser.urls', namespace='browse')),

    url(r'^r/(?P<title>([^/])+)/info$', 'r.views.text_info'),
    url(r'^r/(?P<title>([^/])+)/(?P<file_format>(txt|pdf))$', 'r.views.text_download'),

    url(r'^sparql/(?P<lemma>.*)$', 'sparql.views.index'),

    url(r'^ocr/(?P<ocr_id>[0-9]+)$', 'ocr.views.show_processed'),
    url(r'^ocr/$', 'ocr.views.index'),

    url(r'^search/', include('search.urls', namespace='search')),

    url(r'^documentation/sparql/',
        TemplateView.as_view(template_name='documentation/sparql.html')),
    url(r'^documentation/',
        TemplateView.as_view(template_name='documentation/index.html')),

    url(r'^about/',
        TemplateView.as_view(template_name='about/index.html')),

    url(r'^$', 'roche.views.index'),
)
