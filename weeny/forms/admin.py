# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from weeny.models import WeenyURL


class PasswordInput(forms.PasswordInput):

    # No need to render the entire encrypted string
    # with dotted stars...
    def render(self, name, value, attrs=None):
        if self.render_value and value:
            value = value[:8]
        return super(PasswordInput, self).render(name, value, attrs)


class WeenyURLAdminForm(forms.ModelForm):

    class Meta:
        model = WeenyURL
        widgets = {
            "password": PasswordInput(render_value=True)
        }
