# Create your views here.

from __future__ import unicode_literals

from django.contrib.sites.models import get_current_site
from django.views.generic import RedirectView
from django.views.generic.detail import SingleObjectMixin

from weeny.models import WeenyURL
from weeny.signals import track_visit


class URLRedirectView(SingleObjectMixin, RedirectView):
    """
    A View which redirects to the objects `get_absolute_url`.
    """

    model = WeenyURL
    object = None
    slug_field = "urlcode"
    slug_url_kwarg = "urlcode"

    def get_queryset(self):
        return super(URLRedirectView, self).get_queryset().filter(weeny_site__site=get_current_site(self.request))

    def get_redirect_url(self, *args, **kwargs):
        """
        Return the URL to redirect to.
        """
        self.object = self.get_object()

        if not self.object.is_active or self.object.is_visited and not self.object.allow_revisit:
            return None

        if self.object.weeny_site.track or self.object.track:
            track_visit.send(sender=self.object.__class__, instance=self.object, request=self.request)

        self.object.is_visited = True
        self.object.save()
        return self.object.redirect_url

