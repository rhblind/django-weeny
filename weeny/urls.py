# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import patterns, url

from weeny.views import WeenyURLView


urlpatterns = patterns(
    "",
    url(r"^(?P<urlcode>[a-zA-Z0-9]+)/$", view=WeenyURLView.as_view(), name="weeny_urlcode_view")
)
