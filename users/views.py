from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import *
from django.urls import reverse_lazy


class UserCreateView(CreateView):
    template_name = 'register.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('home')
