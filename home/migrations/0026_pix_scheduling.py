# Generated by Django 5.0.1 on 2024-01-15 19:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_pix_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pix',
            name='scheduling',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.scheduling'),
        ),
    ]
