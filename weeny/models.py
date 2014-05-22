# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random

from django.db import models
from django.db.models import signals, permalink
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


# A constant holding all base62 valid digits
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class WeenySite(models.Model):
    """
    A WeenySite contains the short domain and is linked to a configured
    `django.contrib.sites` site.
    All WeenySites have a unique seed which will be used as a base for
    generating url codes from.
    """

    TRANSFER_PROTOCOL = (
        ("http", "HTTP"),
        ("https", "HTTPS"),
        ("ftp", "FTP"),
        ("ftps", "FTPS")
    )

    site = models.ForeignKey(Site)
    short_domain = models.CharField(verbose_name=_("short domain name"), max_length=50)
    protocol = models.CharField(max_length=10, choices=TRANSFER_PROTOCOL, default="https")
    seed = models.CharField(max_length=62, blank=True, db_index=True, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("date/time created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("date/time updated"))

    class Meta:
        unique_together = ["site", "short_domain"]

    def __unicode__(self):
        return self.short_domain

    def save(self, *args, **kwargs):
        if not self.seed:
            seed = list(BASE62)
            random.seed(random.randint(1, 9999))
            random.shuffle(seed)
            self.seed = "".join(seed)
        super(WeenySite, self).save(*args, **kwargs)


class WeenyURL(models.Model):
    """
    A generic relations model which contains shortned urls for
    any model. Requires that the `content_object` to have a
    `get_absolute_url` method implemented.
    """

    content_type = models.ForeignKey(ContentType, verbose_name=_("content type"),
                                     related_name="contenttype_set_for_%(class)s")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")
    weeny_site = models.ForeignKey(WeenySite, help_text=_("A site which resolves to your short domain name."))
    urlcode = models.CharField(max_length=10, db_index=True, blank=True, verbose_name=_("URL code"),
                               help_text=_("This code will be appended to the weeny domain to "
                                           "create the shortened url."))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("date/time created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("date/time updated"))

    class Meta:
        ordering = ["weeny_site"]
        unique_together = ["weeny_site", "urlcode"]

    def __unicode__(self):
        return "{obj} - {code}".format(obj=self.content_object, code=self.urlcode)

    @property
    def redirect_url(self):
        return "{protocol}://{domain}{uri}".format(
            protocol=self.weeny_site.protocol,
            domain=self.weeny_site.site.domain,
            uri=self.content_object.get_absolute_url()
        )

    def clean(self):
        if not hasattr(self.content_object, "get_absolute_url"):
            raise ValidationError(_(
                "%(cls)r has no `get_absolute_url` method. In order to use django-weeny, "
                "all target objects needs to have a resolvable url. Please implement a `get_absolute_url`"
                "method on %(cls)r in order to target this object." % {"cls": self.content_object.__class__}
            ))


@receiver(signals.post_save, sender=WeenyURL)
def post_save_callback(sender, instance, **kwargs):
    """
    Catch model post-save and create the URL code.

    Disclaimer: This algorithm is shamelessy "stolen" from Drew Perttula!
        http://code.activestate.com/recipes/111286/
    """

    token = 0
    for digit in str(instance.pk):
        token = token * len(BASE62) + BASE62.index(digit)

    if token == 0:
        code = instance.weeny_site.seed[0]
    else:
        code = ""
        while token > 0:
            digit = token % len(instance.weeny_site.seed)
            code = instance.weeny_site.seed[digit] + code
            token = int(token / len(instance.weeny_site.seed))

    # Hacky and expensive solution to update the model without
    # firing the post_save signal again (which will lead to an infinity loop).
    sender.objects.filter(pk=instance.pk).update(urlcode=code)


