from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse_lazy


class HomeView(ListView):
    template_name = 'home.html'
    model = Services
    context_object_name = 'services'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['barbers'] = BarbersTeam.objects.all()
        return context


class ServiceCreateView(CreateView):
    template_name = 'service_create.html'
    model = Services
    form_class = ServiceCreateForm
    success_url = reverse_lazy('home')


class SchedulingCreateView(CreateView):
    template_name = 'scheduling.html'
    model = Scheduling
    form_class = SchedulingForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super().form_valid(form)


class SchedulingUpdateView(UpdateView):
    model = Scheduling
    form_class = SchedulingForm
    template_name = 'scheduling_update.html'
    success_url = reverse_lazy('scheduling_detail')

    def get_success_url(self) -> str:

        return reverse_lazy('scheduling_detail', kwargs={'pk': self.object.pk})


class UserSchedulingListView(ListView):
    model = Scheduling
    template_name = 'user_scheduling.html'
    context_object_name = 'user_scheduling'

    def get_queryset(self):
        return Scheduling.objects.filter(user=self.request.user).order_by('-day')


class UserSchedulingDetailView(DetailView):
    model = Scheduling
    template_name = 'scheduling_detail.html'


class UserSchedulingDeleteView(DeleteView):
    model = Scheduling
    template_name = 'scheduling_delete.html'
    success_url = reverse_lazy('home')


class PortfolioCreateView(CreateView):
    model = Portfolio
    template_name = 'portfolio_create.html'
    form_class = PortfolioForm

    def get_success_url(self) -> str:
        return reverse_lazy(f'portfolio', kwargs={'pk': self.object.pk})


class PortfolioListView(ListView):
    model = Portfolio
    template_name = 'portfolio_list.html'
    context_object_name = 'portfolio_objects'
