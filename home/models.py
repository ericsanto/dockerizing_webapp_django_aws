from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


class Services(models.Model):
    name = models.CharField(verbose_name='Nome',
                            max_length=255, blank=True, null=True)
    price = models.FloatField(verbose_name='Preço', blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='serviços')

    class Meta:
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name or ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            new_width = 18 * 16
            new_heigth = 200

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

    def __str__(self):
        return self.user.username


class Portfolio(models.Model):
    description = models.TextField(blank=True, null=True)
    image_portfolio = models.ImageField(
        blank=True, null=True, upload_to='portfolio')
