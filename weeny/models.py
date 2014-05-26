# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random

from user_agents.parsers import parse as ua_parse

from django.db import models
from django.db.models import signals
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.sites.models import Site
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from weeny import logger
from weeny.signals import track_visit

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
    redirect_short_domain = models.BooleanField(default=False, help_text=_("Check to make URL's for this site "
                                                                           "redirect to the short domain."))
    protocol = models.CharField(max_length=10, choices=TRANSFER_PROTOCOL, default="https")
    requires_moderation = models.BooleanField(default=False, help_text=_("Check to require URL's for this site to "
                                                                         "be moderated before being usable."))
    track = models.BooleanField(default=False, help_text=_("Track all URL's for this site."))
    seed = models.CharField(max_length=62, blank=True, db_index=True, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("date/time created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("date/time modified"))

    class Meta:
        unique_together = ["site", "short_domain"]

    def __unicode__(self):
        return "{0} - {1}".format(self.short_domain, self.site.domain)

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
    track = models.BooleanField(default=False, help_text=_("Check to track visits to this URL."))
    allow_revisit = models.BooleanField(default=True, help_text=_("Check to allow URL to be used multiple times"))
    is_active = models.BooleanField(default=True, verbose_name=_("active"), help_text=_("Check to activate the URL."))
    is_visited = models.BooleanField(default=False, verbose_name=_("visited"))
    is_private = models.BooleanField(default=False, verbose_name=_("private URL"),
                                     help_text=_("Check this if you want the URL to be password protected."))
    is_removed = models.BooleanField(default=False, verbose_name=_("removed"),
                                     help_text=_("Check this box if the URL should be considered removed. "
                                                 "A `This URL has been removed` message will be displayed instead."))
    password = models.CharField(max_length=128, blank=True, null=True,
                                help_text=_("Only required if private URL. This password is stored encrypted and there "
                                            "is no way of retrieving it. Keep that in mind =)"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("date/time created"))
    modified = models.DateTimeField(auto_now=True, verbose_name=_("date/time modified"))

    class Meta:
        ordering = ["weeny_site"]
        unique_together = ["weeny_site", "urlcode"]
        permissions = [("can_moderate", "Can moderate Weeny URL's")]

    def __unicode__(self):
        return "{obj} - {code}".format(obj=self.content_object, code=self.urlcode)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse_lazy
        return reverse_lazy("weeny_urlredirect_view", kwargs={"urlcode": self.urlcode})

    @property
    def redirect_url(self):
        return "{protocol}://{domain}{uri}".format(
            protocol=self.weeny_site.protocol,
            domain=self.weeny_site.short_domain if self.weeny_site.redirect_short_domain
                else self.weeny_site.site.domain,
            uri=self.content_object.get_absolute_url()
        )

    def clean(self):
        if not hasattr(self.content_object, "get_absolute_url"):
            raise ValidationError(_(
                "%(cls)r has no `get_absolute_url` method. In order to use django-weeny, "
                "all target objects needs to have a resolvable url. Please implement a `get_absolute_url`"
                "method on %(cls)r in order to target this object." % {"cls": self.content_object.__class__}
            ))

        if self.is_private:
            if not self.password:
                raise ValidationError(_("Private URL's needs a password!"))
            self.password = make_password(self.password)

        if self.password and not self.is_private:
            raise ValidationError(_("You can't set password on public URL's!"))


class UserAgent(models.Model):
    """
    Keep track of user agents.
    """

    ua_string = models.TextField(verbose_name=_("user agent string"))
    browser_family = models.CharField(max_length=50)
    browser_version = models.CharField(max_length=20)
    device_family = models.CharField(max_length=50)
    os_family = models.CharField(max_length=50, verbose_name=_("OS family"))
    os_version = models.CharField(max_length=20, verbose_name=_("OS version"))
    is_bot = models.BooleanField(default=False, verbose_name=_("bot"))
    is_mobile = models.BooleanField(default=False, verbose_name=_("mobile"))
    is_pc = models.BooleanField(default=False, verbose_name=_("PC"))
    is_tablet = models.BooleanField(default=False, verbose_name=_("tablet"))
    is_touch_capable = models.BooleanField(default=False, verbose_name=_("touch capable"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["browser_family", "os_family", "browser_version", "os_version"]

    def __unicode__(self):
        return "{browser} {version}".format(browser=self.browser_family, version=self.browser_version)


class URLTracking(models.Model):
    """
    This model will store records of visits to URLs
    if URL tracking is enabled on the model.
    """

    url = models.ForeignKey(WeenyURL)
    weeny_site = models.ForeignKey(WeenySite)
    weeny_url = models.CharField(max_length=255)
    target_url = models.CharField(max_length=255)
    ip_address = models.IPAddressField()
    user_agent = models.ForeignKey(UserAgent)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = "URL tracking"
        ordering = ["weeny_url", "weeny_site__site", "timestamp", "user_agent"]

    def __unicode__(self):
        return "{weeny_url} - {ip_address}".format(weeny_url=self.weeny_url, ip_address=self.ip_address)


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

@receiver(track_visit, sender=WeenyURL)
def track_visit_callback(sender, instance, request, **kwargs):
    """
    Create URL tracking records!
    """

    user_agent = ua_parse(request.META["HTTP_USER_AGENT"])
    user_agent_obj, created = UserAgent.objects.get_or_create(ua_string=user_agent.ua_string, defaults={
        "ua_string": user_agent.ua_string,
        "browser_family": user_agent.browser.family,
        "browser_version": user_agent.browser.version_string,
        "device_family": user_agent.device.family,
        "os_family": user_agent.os.family,
        "os_version": user_agent.os.version_string,
        "is_bot": user_agent.is_bot,
        "is_mobile": user_agent.is_mobile,
        "is_pc": user_agent.is_pc,
        "is_tablet": user_agent.is_tablet,
        "is_touch_capable": user_agent.is_touch_capable
    })

    if created:
        logger.info(
            "Created new UserAgent {browser_family} - {browser_version} "
            "({os_family} - {os_version}).".format(
                browser_family=user_agent_obj.browser_family,
                browser_version=user_agent_obj.browser_version,
                os_family=user_agent_obj.os_family,
                os_version=user_agent_obj.os_version
            )
        )

    URLTracking.objects.create(**{
        "url": instance,
        "weeny_site": instance.weeny_site,
        "weeny_url": instance.get_absolute_url(),
        "target_url": instance.redirect_url,
        "ip_address": request.META["REMOTE_ADDR"],
        "user_agent": user_agent_obj
    })
