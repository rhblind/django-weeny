# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.dispatch import Signal

# Sent when a visitor is redirected to the target URL,
# and URL tracking is enabled for either the URL or the
# weeny site the URL belongs to.
track_visit = Signal(providing_args=["instance", "request"], use_caching=True)
