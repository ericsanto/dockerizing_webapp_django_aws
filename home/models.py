from django.db import models
from django.conf import settings
from django.utils import timezone
from PIL import Image
from django.contrib import messages
from django.db.models import Sum, Max, Count, Min
from datetime import datetime
from users.models import UserCustom


class Services(models.Model):
    name = models.CharField(verbose_name='Nome',
                            max_length=255, blank=True, null=True)
    price = models.DecimalField(verbose_name='Preço',
                                blank=True, null=True, default=0, decimal_places=2, max_digits=5)
    image = models.ImageField(blank=True, null=True, upload_to='serviços')

    class Meta:
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name or ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            new_width = 122
            new_heigth = 117

            img = img.resize((new_width, new_heigth), Image.ADAPTIVE)
            img.save(self.image.path)

        return min


TIMES = (
    ("1", "08:00 às 09:00"),
    ("2", "09:00 às 10:00"),
    ("3", "10:00 às 11:00"),
    ("4", "11:00 às 12:00"),
    ("5", "14:00 às 15:00"),
    ("6", "15:00 às 16:00"),
    ("7", "16:00 às 17:00"),
    ("8", "17:00 às 18:00"),
    ("9", "18:00 às 19:00"),
)


class BarbersTeam(models.Model):
    name = models.CharField(max_length=255, blank=True,
                            null=True, verbose_name='Barbeiro(a)')
    photo = models.ImageField(blank=True, null=True, upload_to='foto_barbeiro')

    class Meta:
        verbose_name_plural = 'Barbers Team'

    def __str__(self):
        return self.name


class Scheduling(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Cliente', on_delete=models.CASCADE)
    day = models.DateField(verbose_name='Dia')
    service = models.ForeignKey(
        Services, verbose_name='Serviço', on_delete=models.CASCADE)
    time = models.CharField(
        max_length=255, verbose_name='Horários', choices=TIMES, blank=True, null=True)
    barber = models.ForeignKey(
        BarbersTeam, blank=True, null=True, on_delete=models.CASCADE)
    phone = models.CharField('Celular', max_length=16, blank=True, null=True)
    paid = models.BooleanField(verbose_name='Pago', default=False)

    def __str__(self):
        return self.user.username or ''

    @staticmethod
    def show_day():
        return timezone.now().date()

    def count_scheduling(self):
        date = datetime.now()
        month = date.month

        mont_scheduling = Scheduling.objects.filter(
            day__month=month).aggregate(Count('service'))['service__count']
        return mont_scheduling


class Portfolio(models.Model):
    description = models.TextField(blank=True, null=True)
    image_portfolio = models.ImageField(
        blank=True, null=True, upload_to='portfolio')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image_portfolio:
            img = Image.open(self.image_portfolio.path)

            new_width = 20 * 20
            new_heigth = 250

            img = img.resize((new_width, new_heigth), Image.ADAPTIVE)
            img.save(self.image_portfolio.path)


class Finance(models.Model):
    scheduling = models.ForeignKey(
        Scheduling, verbose_name='Todos os Agendamentos:', blank=True, null=True, on_delete=models.CASCADE)

    def total_value(self):
        total = Scheduling.objects.filter(paid=True).aggregate(
            Sum('service__price'))['service__price__sum']
        return total

    def total_scheduling(self):
        total = Scheduling.objects.all().count()
        return total

    def total_scheduling_paid(self):
        total = Scheduling.objects.filter(paid=True).count()
        return total

    def total_scheduling_user(self):
        total = UserCustom.objects.filter
        return total

    def max_value_service_scheduling(self):
        total = Scheduling.objects.filter(paid=True).aggregate(
            Max('service__price'))['service__price__max']
        return total
