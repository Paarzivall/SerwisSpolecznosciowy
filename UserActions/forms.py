from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    name = forms.CharField(max_length=254, help_text='Podaj imie...')
    surname = forms.CharField(max_length=254, help_text='Podaj nazwisko...')
    new_login = forms.CharField(max_length=254, help_text='Podaj login...')
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=254, help_text='Podaj email...')

    class Meta:
        model = User
        fields = ('name', 'surname', 'new_login', 'email', 'password')
