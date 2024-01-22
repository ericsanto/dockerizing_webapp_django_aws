from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create_service/', ServiceCreateView.as_view(), name='create_service'),
    path('scheduling/', SchedulingCreateView.as_view(), name='scheduling'),
    path('scheduling_update/<int:pk>/',
         SchedulingUpdateView.as_view(), name='scheduling_update'),
    path('scheduling_user/', UserSchedulingListView.as_view(),
         name='scheduling_user'),
    path('scheduling_detail/<int:pk>/',
         UserSchedulingDetailView.as_view(), name='scheduling_detail'),
    path('scheduling_delete/<int:pk>/',
         UserSchedulingDeleteView.as_view(), name='scheduling_delete'),
    path('portfolio_create/', PortfolioCreateView.as_view(),
         name='portfolio_create'),
    path('portfolio/', PortfolioListView.as_view(), name='portfolio'),
    path('restrict/finances/', FinanceListView.as_view(), name='finances'),
    path('scheduling_to_day/', SchedulingToDay.as_view(), name='scheduling_to_day'),
    path('scheduling_to_month/', SchedulingToMonth.as_view(), name='scheduling_to_month'),

]
