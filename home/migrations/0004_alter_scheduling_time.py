# Generated by Django 5.0.1 on 2024-01-03 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_scheduling_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduling',
            name='time',
            field=models.CharField(blank=True, choices=[('1', '08:00 às 09:00'), ('2', '09:00 às 10:00'), ('3', '10:00 às 11:00'), ('4', '11:00 às 12:00'), ('5', '14:00 às 15:00'), ('6', '15:00 às 16:00'), ('7', '16:00 às 17:00'), ('8', '17:00 às 18:00'), ('9', '18:00 às 19:00')], max_length=255, null=True, verbose_name='Horários'),
        ),
    ]
