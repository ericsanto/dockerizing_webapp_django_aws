from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from django.contrib import messages


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
        User, verbose_name='Cliente', on_delete=models.CASCADE)
    day = models.DateField(verbose_name='Dia')
    service = models.ForeignKey(
        Services, verbose_name='Serviço', on_delete=models.CASCADE)
    time = models.CharField(
        max_length=255, verbose_name='Horários', choices=TIMES, blank=True, null=True)
    barber = models.ForeignKey(
        BarbersTeam, blank=True, null=True, on_delete=models.CASCADE)
    phone = models.CharField('Celular', max_length=16, blank=True, null=True)
    scheduling_complete = models.BooleanField(
        default=False, blank=True, null=True)
    scheduling_quantity = models.PositiveIntegerField(
        default=0, blank=True, null=True)

    def __str__(self):
        return self.user.username or ''

    @staticmethod
    def show_day():
        return timezone.now().date()


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
        return sum(self.scheduling.service.price for self.scheduling in Scheduling.objects.all())


class Carrousel(models.Model):
    image_carrousel = models.ImageField(
        upload_to='carrousel_images', blank=True, null=True)
    title_carousel = models.CharField(
        'Título do Carrousel:', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title_carousel

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image_carrousel:
            image = Image.open(self.image_carrousel.path)

            new_width = 25 * 25
            new_heigth = 350

            image.resize((new_width, new_heigth), Image.ADAPTIVE)
            image.save(self.image_carrousel.path)
