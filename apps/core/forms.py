from django import forms
from apps.core.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

class UserRegForm(UserCreationForm):
    """Form definition for UserReg."""

    class Meta:
        """Meta definition for UserRegform."""

        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Email'),
            'username':_('Username'),
        }

        localize_fields = "__all__"

        error_messages = {
            'email': {
                'unique': _("The email provided is already taken!"),
                },
            'first_name': {
                'max_lenght': _("This first name is too long!")
            }, 
            'last_name': {
                'min_length': _("Full name too short")
            }
        }