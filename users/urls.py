from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('create_user/',  UserCreateView.as_view(), name='create_user'),
    path('login_user/', LoginView.as_view(
        template_name='login.html'), name='login'),
    path('logout_user/', LogoutView.as_view(
        template_name='logout.html'), name='logout'),
]
