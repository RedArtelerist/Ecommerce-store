from itertools import chain

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import RadioSelect
from django.utils.encoding import force_text

from orders.utils import queryset_cities
from user_profile.models import Profile


class RadioSelectNotNull(RadioSelect):
    def get_renderer(self, name, value, attrs=None, choices=()):
        """Returns an instance of the renderer."""
        if value is None: value = ''
        str_value = force_text(value) # Normalize to string.
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(self.choices, choices))
        if choices[0][0] == '':
            choices.pop(0)
        return self.renderer(name, str_value, final_attrs, choices)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'last name'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['middle_name', 'gender', 'birthdate', 'city', 'phone', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'id': 'imageUpload'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'middle name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'data-name': 'mobile phone'}),
            'city': forms.Select(choices=queryset_cities(), attrs={'class': 'form-control', 'data-name': 'city'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'data-name': 'birthdate'}),
            'gender': forms.RadioSelect(attrs={'class': 'custom-control-input'})
        }


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class ChangeUserNameForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username']