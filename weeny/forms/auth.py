# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


class AuthenticateForm(forms.Form):
    """
    Really basic form for authenticating a password
    for a Weeny URL.
    """

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.object = kwargs.pop("object")
        super(AuthenticateForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]
        valid_password = check_password(
            force_text(password), self.object.password)
        if not valid_password:
            raise ValidationError(_("Invalid password!"))
        return password

