# Create your views here.

from __future__ import unicode_literals

from django import http
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, FormView
from django.views.generic.detail import SingleObjectMixin

from weeny import logger
from weeny.models import WeenyURL
from weeny.forms.auth import AuthenticateForm
from weeny.signals import track_visit


class URLRedirectView(SingleObjectMixin, FormView, RedirectView):
    """
    Redirects the user to the target URL.
    """

    model = WeenyURL
    object = None
    slug_field = "urlcode"
    slug_url_kwarg = "urlcode"
    form_class = AuthenticateForm
    authenticate_url = reverse_lazy("weeny_authenticate_view")
    template_name = "weeny/authenticate.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(URLRedirectView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.object.is_private:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(self.get_context_data(form=form))
        else:
            url = self.get_redirect_url(*args, **kwargs)
            if url:
                if self.permanent:
                    return http.HttpResponsePermanentRedirect(url)
                else:
                    return http.HttpResponseRedirect(url)
            else:
                logger.warning("Gone: %s", self.request.path,
                               extra={
                                   "status_code": 410,
                                   "request": self.request
                               })
                return http.HttpResponseGone()

    def get_form_kwargs(self):
        kwargs = super(URLRedirectView, self).get_form_kwargs()
        kwargs["object"] = self.object
        return kwargs

    def get_success_url(self):
        self.success_url = self.get_redirect_url()
        return super(URLRedirectView, self).get_success_url()

    def get_redirect_url(self, *args, **kwargs):
        if not self.object.is_active or self.object.is_visited and not self.object.allow_revisit:
            return None

        if self.object.weeny_site.track or self.object.track:
            track_visit.send(sender=self.object.__class__, instance=self.object, request=self.request)

        self.object.is_visited = True
        self.object.save()
        return self.object.redirect_url

    def get_queryset(self):
        return super(URLRedirectView, self).get_queryset().filter(weeny_site__site=get_current_site(self.request))
