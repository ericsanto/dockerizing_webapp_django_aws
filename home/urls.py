from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create_service/', ServiceCreateView.as_view(), name='create_service'),
    path('scheduling/', SchedulingCreateView.as_view(), name='scheduling'),
]
