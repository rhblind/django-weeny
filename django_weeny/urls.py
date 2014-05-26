# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_weeny.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^weeny/', include("weeny.urls"))
)

if settings.DEBUG is True:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
