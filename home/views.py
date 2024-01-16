from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import datetime


class HomeView(ListView):
    template_name = 'home.html'
    model = Services
    context_object_name = 'services'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['barbers'] = BarbersTeam.objects.all()
        context['carousel'] = Carrousel.objects.all()
        return context


class ServiceCreateView(UserPassesTestMixin, CreateView):
    template_name = 'service_create.html'
    model = Services
    form_class = ServiceCreateForm
    success_url = reverse_lazy('home')


class SchedulingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'scheduling.html'
    model = Scheduling
    form_class = SchedulingForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            messages.success(self.request, 'Agendamento marcado com Sucesso')

        return super().form_valid(form)


class SchedulingUpdateView(LoginRequiredMixin, UpdateView):
    model = Scheduling
    form_class = SchedulingForm
    template_name = 'scheduling_update.html'
    success_url = reverse_lazy('scheduling_detail')

    def get_success_url(self) -> str:

        return reverse_lazy('scheduling_detail', kwargs={'pk': self.object.pk})


class UserSchedulingListView(LoginRequiredMixin, ListView):
    model = Scheduling
    template_name = 'user_scheduling.html'
    context_object_name = 'user_scheduling'

    def get_queryset(self):
        return Scheduling.objects.filter(user=self.request.user).order_by('-day')


class UserSchedulingDetailView(LoginRequiredMixin, DetailView):
    model = Scheduling
    template_name = 'scheduling_detail.html'


class UserSchedulingDeleteView(LoginRequiredMixin, DeleteView):
    model = Scheduling
    template_name = 'scheduling_delete.html'
    success_url = reverse_lazy('home')


class PortfolioCreateView(UserPassesTestMixin, CreateView):
    model = Portfolio
    template_name = 'portfolio_create.html'
    form_class = PortfolioForm

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self) -> str:
        return reverse_lazy(f'portfolio', kwargs={'pk': self.object.pk})


class PortfolioListView(ListView):
    model = Portfolio
    template_name = 'portfolio_list.html'
    context_object_name = 'portfolio_objects'


class FinanceListView(UserPassesTestMixin, ListView):
    model = Finance
    template_name = 'finances.html'
    context_object_name = 'finances_objects'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['finances'] = Finance()
        return context


class SchedulingToDay(UserPassesTestMixin, ListView):
    model = Scheduling
    template_name = 'list_scheduling_to_day.html'
    context_object_name = 'scheduling_to_day'

    def get_queryset(self):
        day_now = timezone.now().date()
        schedulings_to_day = Scheduling.objects.filter(day=day_now)
        return schedulings_to_day

    def test_func(self):
        return self.request.user.is_superuser


class PayToPixListView(ListView):
    model = Pix
    template_name = 'pay_to_pix.html'
    context_object_name = 'pix'
