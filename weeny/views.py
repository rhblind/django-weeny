# Create your views here.

from __future__ import unicode_literals

from django.contrib.sites.models import get_current_site
from django.views.generic import RedirectView
from django.views.generic.detail import SingleObjectMixin

from weeny.models import WeenyURL


class WeenyURLView(SingleObjectMixin, RedirectView):
    """
    A View which redirects to the objects `get_absolute_url`.
    """

    model = WeenyURL
    object = None
    slug_field = "urlcode"
    slug_url_kwarg = "urlcode"

    def get_queryset(self):
        return super(WeenyURLView, self).get_queryset().filter(weeny_site__site=get_current_site(self.request))

    def get_redirect_url(self, *args, **kwargs):
        """
        Return the URL to redirect to.
        """
        self.object = self.get_object()
        try:
            url = self.object.redirect_url
        except AttributeError as e:
            # If for some reason the user has managed to create a
            # WeenyURL for an object which has not `get_absolute_url`
            # it will raise an AttributeError. Log, and carry on!
            # TODO: Log this!
            return None

        return url

