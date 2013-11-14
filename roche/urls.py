# coding=utf-8
#

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView


browser_patters = patterns('',
    url(r'^$', TemplateView.as_view(template_name='browser/index.html')),
)

urlpatterns = i18n_patterns('',
    url(r'^$', TemplateView.as_view(template_name='roche/index.html')),
    url(r'^browse/$', include(browser_patters, namespace='browse')),
)
