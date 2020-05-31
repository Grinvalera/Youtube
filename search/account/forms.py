from django import forms
from django.forms import ModelForm
from django.contrib.auth.views import UserModel


class RegistrationForm(ModelForm):
    class Meta:
        model = UserModel
        exclude = ('_password', '_password2')

    _password = forms.CharField(label='Password', widget=forms.PasswordInput)
    _password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_password(self):
        cd = self.cleaned_data
        if cd['_password'] == ['_password2']:
            return cd['_password2']
        else:
            return forms.ValidationError('Password don\'t match.')