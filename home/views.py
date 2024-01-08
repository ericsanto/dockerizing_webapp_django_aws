from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DeleteView, CreateView, UpdateView
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
    template_name = 'scheduling_'
    pass
