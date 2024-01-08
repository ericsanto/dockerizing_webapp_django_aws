from django import forms
from .models import *
from django.forms import ValidationError
from datetime import date


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
        fields = ('day', 'service', 'time')

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

        if Scheduling.objects.filter(time=time).exists():
            raise forms.ValidationError(f'O horário está indisponível')
        return time
