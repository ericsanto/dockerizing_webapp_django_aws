from django.shortcuts import render, redirect
from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
import datetime
from datetime import datetime
import mercadopago
from core.settings import *
from django.shortcuts import get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid


class HomeView(ListView):
    template_name = 'home.html'
    model = Services
    context_object_name = 'services'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['barbers'] = BarbersTeam.objects.all()
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

    def get_success_url(self):
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
        context['finance'] = Finance()
        context['scheduling'] = Scheduling()

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


class SchedulingToMonth(ListView):
    model = Scheduling
    template_name = 'scheduling_to_month.html'
    context_object_name = 'scheduling_to_month'

    def get_queryset(self):
        day = datetime.now()
        month = day.month
        month_filter = self.request.GET.get('month')

        if month_filter:
            month_resp = Scheduling.objects.filter(
                day__month=int(month_filter))
            return month_resp
        else:
            month_all = Scheduling.objects.filter(day__month=month)
            return month_all

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['finance'] = Finance()
        return context


"""def iniciar_pagamento(request, scheduling_id):

    scheduling = get_object_or_404(Scheduling, pk=scheduling_id)
    sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)

    price = float(scheduling.service.price)

    preference_data = {
        "items": [
            {
                "title": scheduling.service.name,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": price,
            }
        ]
    }

    # Cria a preferência de pagamento
    preference_response = sdk.preference().create(preference_data)
    if 'response' in preference_response:
        preference = preference_response['response']

    else:
        preference = None

    return render(request, 'iniciar_pagamento.html', {'preference':  preference})"""


"""def payment(request, scheduling_id):

    paypal_client_id = PAYPAL_CLIENT_ID
    paypal_secret_key = PAYPAL_SECRET_KEY

    scheduling = get_object_or_404(Scheduling, pk=scheduling_id)
    price = float(scheduling.service.price)

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/success/",
            "cancel_url": "http://localhost:8000/cancel/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": scheduling.service.name,
                    "sku": "item123",
                    "price": price,
                    "currency": "BRL",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "5.00",
                "currency": "BRL"
            },
            "description": "Compra de teste"
        }]
    }, api=paypalrestsdk.set_config({
        'mode': 'sandbox',  # ou 'live' para ambiente de produção
        'client_id': paypal_client_id,
        'client_secret': paypal_secret_key
    }))

    if payment.create():
        # Redirecione para a URL de aprovação do PayPal
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)
    return render(request, 'payment.html', {'payment': payment})"""


def CheckOut(request, scheduling_id):
    scheduling = Scheduling.objects.get(id=scheduling_id)

    host = request.get_host()

    paypal_checkout = {
        'business': PAYPAL_RECEIVER_EMAIL,
        'amount': scheduling.service.price,
        'item_name': scheduling.service.name,
        'invoice': uuid.uuid4(),
        'currency_code': 'BRL',
        'notify_url': f'https://{host}{reverse("paypal-ipn")}',
        'return_url': f'https://{host}{reverse("payment_successfull", kwargs={"scheduling_id": scheduling.id})}',
        # 'cancel_url': f'https://{host}{reverse("payment_failed", kwargs={"scheduling_id": scheduling.id})}'
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'scheduling': scheduling,
        'paypal': paypal_payment
    }

    return render(request, 'checkout.html', context)


def PaymentSuccessfull(request, scheduling_id):
    scheduling = get_object_or_404(Scheduling, pk=scheduling_id)

    context = {
        'scheduling': scheduling
    }

    return render(request, 'payment_successful.html', context)
