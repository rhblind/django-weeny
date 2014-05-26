# -*- coding: utf-8 -*-

from django.contrib import admin
from weeny.forms.admin import WeenyURLAdminForm
from weeny.models import WeenySite, WeenyURL, URLTracking, UserAgent


class WeenySiteAdmin(admin.ModelAdmin):
    readonly_fields = ["seed"]
    list_display = ["short_domain", "site", "track", "redirect_short_domain",
                    "requires_moderation", "seed", "created"]


class WeenyURLAdmin(admin.ModelAdmin):
    form = WeenyURLAdminForm
    readonly_fields = ["urlcode", "is_visited", "created", "modified"]
    list_display = ["weeny_url", "redirect_url", "is_active", "is_private",
                    "content_type", "content_object", "weeny_site", "target_site"]
    list_filter = ["weeny_site__site", "weeny_site", "is_active", "is_visited", "is_private"]
    search_fields = ["urlcode"]

    fieldsets = (
        (None, {
            "fields": ("weeny_site", "content_type", "object_id",
                       "is_visited", "urlcode", "created", "modified")
        }),
        ("Privacy", {
            "fields": ("is_private", "password", "track")
        }),
        ("Moderation", {
            "fields": ("is_active", "allow_revisit")
        })
    )

    @staticmethod
    def weeny_url(obj):
        return obj.get_absolute_url()

    @staticmethod
    def redirect_url(obj):
        return obj.redirect_url

    @staticmethod
    def target_site(obj):
        return obj.weeny_site.site


class URLTrackingAdmin(admin.ModelAdmin):
    list_display = ["weeny_url", "target_url", "ip_address", "weeny_site",
                    "user_agent", "timestamp"]
    list_filter = ["weeny_site__site", "weeny_site"]
    fieldsets = (
        (None, {
            "fields": ("weeny_url", "weeny_site", "target_url",
                       "ip_address", "user_agent", "timestamp")
        }),
    )

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))


class UserAgentAdmin(admin.ModelAdmin):
    list_display = ["browser_family", "browser_version", "device_family", "os_family", "os_version"]
    list_filter = search_fields = ["browser_family", "device_family", "os_family"]
    fieldsets = (
        (None, {
            "fields": ("browser_family", "browser_version", "device_family",
                       "os_family", "os_version", "ua_string")
        }),
        ("Meta", {
            "fields": ("is_bot", "is_mobile", "is_pc", "is_tablet", "is_touch_capable")
        })
    )

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))


admin.site.register(WeenySite, WeenySiteAdmin)
admin.site.register(WeenyURL, WeenyURLAdmin)
admin.site.register(URLTracking, URLTrackingAdmin)
admin.site.register(UserAgent, UserAgentAdmin)
