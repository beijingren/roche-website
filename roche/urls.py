# coding=utf-8

from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView


urlpatterns = i18n_patterns('',
    url(r'^browse/', include('browser.urls', namespace='browse')),
    url(r'^browse/text/(?P<title>.*)$', 'browser.views.text_view'),
    url(r'^ocr/', include('ocr.urls', namespace='ocr')),
    url(r'^wiki/', include('djiki.urls')),

    url(r'^$', TemplateView.as_view(template_name='roche/index.html')),
)
