# Generated by Django 5.0.1 on 2024-01-09 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_remove_scheduling_quantity_service_completed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finance',
            name='amount',
        ),
    ]
