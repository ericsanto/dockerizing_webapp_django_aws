from django.shortcuts import render
from django.conf import settings
from django.views.generic import CreateView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView


class UserCreateView(CreateView):
    template_name = 'register.html'
    model = settings.AUTH_USER_MODEL
    form_class = UserForm
    success_url = reverse_lazy('home')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
