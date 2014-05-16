# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class WeenySite(models.Model):
    """

    """

    site = models.ForeignKey(Site)
    peewee_name = models.CharField(verbose_name=_("display name"), max_length=50)
    peewee_domain = models.CharField(verbose_name=_("domain name"), max_length=100)


class WeenyURL(models.Model):
    """

    """

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, verbose_name=_("content type"),
                                     related_name="contenttype_set_for_%(class)s")
    content_object = generic.GenericForeignKey("content_type", "object_id")
    weeny_site = models.ForeignKey(WeenySite)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("date/time created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("date/time updated"))
