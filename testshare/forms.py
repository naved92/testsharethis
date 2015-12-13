import re
from gi.overrides.keysyms import blank

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from testshare.models import UserProfile

class RegistrationForm(forms.Form):
    """
    The Registration form class containing username,email,password,confirm password fields
    """
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
 
    def clean_username(self):
        """
        A username validation method
        :return: validates the user
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        """
        A password validation method
        :return: validates the passwords if confirmed rightly
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class UpdateProfileForm(forms.Form):
    """
    The update profile form class containing password,confirm password fields

    """
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(max_length=30, render_value=False)), label=_("Password (again)"))

    def clean(self):

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class VerificationForm(forms.Form):
    """
    The validation form class containing validation key field

    """
    verification_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'required': 'true',
                                                                      'placeholder': 'enter your verification code'}),
                                        max_length=128, label=_("verification_code"),
                                        help_text='verification code')

    def clean(self):
        return self.cleaned_data


class PasswordChangeForm(forms.Form):
    """
    The Password change form class containingg ,password,confirm password fields

    """
    password_old = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'required': 'true'}),
                                   label=_("Old Password"))
    password_1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                   'required': 'true'}),
                                   label=_("New Password"))
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                   'required': 'true'}),
                                   label=_("New Password (again)"))

    def clean(self):
        return self.cleaned_data