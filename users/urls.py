from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as as_view

urlpatterns = [
    path('create_user/',  UserCreateView.as_view(), name='create_user'),
    path('login_user/', as_view.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('logout/', as_view.LogoutView.as_view(), name='logout'),
]
