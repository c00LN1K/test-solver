from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Придумайте логин', widget=forms.TextInput(attrs={}))
    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={}))
    first_name = forms.CharField(label='Ваше имя')

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'password1', 'password2']
        labels = {'email': 'Email'}
