from django.shortcuts import render
from django.conf import settings
from django.views.generic import CreateView
from .forms import *
from django.urls import reverse_lazy


class UserCreateView(CreateView):
    template_name = 'register.html'
    model = settings.AUTH_USER_MODEL
    form_class = UserForm
    success_url = reverse_lazy('home')
