# -*- coding: utf-8 -*-

from django.contrib import admin
from weeny.models import WeenySite, WeenyURL


class WeenySiteAdmin(admin.ModelAdmin):
    readonly_fields = ["seed"]
    list_display = ["short_domain", "site", "seed", "created"]


class WeenyURLAdmin(admin.ModelAdmin):
    readonly_fields = ["urlcode"]
    list_display = ["content_object", "urlcode", "weeny_site", "real_site"]

    @staticmethod
    def real_site(obj):
        return obj.weeny_site.site

admin.site.register(WeenySite, WeenySiteAdmin)
admin.site.register(WeenyURL, WeenyURLAdmin)
