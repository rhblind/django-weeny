# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import patterns, url

from weeny.views import URLRedirectView


urlpatterns = patterns(
    "",
    url(r"^(?P<urlcode>[a-zA-Z0-9]+)/$", view=URLRedirectView.as_view(), name="weeny_urlredirect_view")
)
