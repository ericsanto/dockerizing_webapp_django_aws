from typing import Any
from django import forms
from .models import *
from django.forms import ValidationError
from datetime import date
import phonenumbers


class ServiceCreateForm(forms.ModelForm):

    class Meta:
        model = Services
        fields = '__all__'

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if int(price) <= 0:
            raise forms.ValidationError(
                'Preço Inválido. O serviço deve ter o preço acima de R$0')
        return price

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError(
                'Não é possível cadastrar o Serviço. Pois, o campo está vazio.')
        return name


class SchedulingForm(forms.ModelForm):

    class Meta:
        model = Scheduling
        fields = ('day', 'service', 'time', 'barber', 'phone')

    def clean_day(self):
        day = self.cleaned_data.get('day')

        if day < timezone.now().date():
            raise forms.ValidationError(
                'Não é possível agendar para dias atrasados')
        return day

    def clean_time(self):
        time = self.cleaned_data.get('time')
        day = self.cleaned_data.get('day')

        if day == timezone.now().date() and time < timezone.now().strftime('%H:%M'):
            raise forms.ValidationError(
                f'Não é possível agendar para o horário , pois já passou!')

        if Scheduling.objects.filter(time=time).exists() and Scheduling.objects.filter(day=day).exists():
            raise forms.ValidationError(
                f'O horário está indisponível para este dia')
        return time

    def save(self, commit=True):
        scheduling = super().save(commit=False)

        if commit:
            scheduling.save()
            Finance.objects.create(
                scheduling=scheduling,
            )
        return scheduling

    '''def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        try:
            phone_parse = phonenumbers.parse(phone, '+55')

            phonenumbers.is_valid_number(phone_parse)
        except:
            raise forms.ValidationError('Número de Celular está incorreto')

        return phone'''


class PortfolioForm(forms.ModelForm):

    class Meta:
        model = Portfolio
        fields = '__all__'
