# Generated by Django 5.0.1 on 2024-01-09 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_scheduling_scheduling_complete_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduling',
            name='scheduling_quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
