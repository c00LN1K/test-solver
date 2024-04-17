from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView

from .forms import *
from .models import Profile


# from django.urls import reverse_lazy


# Create your views here.

class LoginUser(LoginView):
    template_name = 'users/logister.html'
    form_class = LoginForm
    extra_context = {'title': 'Авторизация'}


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user = form.save()
            Profile.objects.create(user=user)
            return render(request, 'users/register_done.html', context={'title': 'Успешная регистрация'})
    else:
        form = RegisterUserForm()

    return render(request, 'users/logister.html', context={'form': form, 'title': 'Регистрация'})


# class RegisterUser(CreateView):
#     template_name = 'users/logister.html'
#     form_class = RegisterUserForm
#     extra_context = {'title': 'Авторизация'}
#     success_url = reverse_lazy('users:login')
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         Profile.objects.create(user=get_user_model().objects.get(username=form.cleaned_data['username']))
#         return response
