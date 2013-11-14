# coding=utf-8
#

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

urlpatterns = i18n_patterns('',
    url(r'^$', TemplateView.as_view(template_name='roche/index.html')),
)
