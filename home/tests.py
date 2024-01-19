from django.test import TestCase, Client
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import date
from django.urls import reverse
from users.models import UserCustom


class SchedulingModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='jujuba', email='jujuba@gmail.com', password='testepassword',
        )

        self.service = Services.objects.create(name='Test Service')
        self.barber = BarbersTeam.objects.create(
            name='Barber Teste'
        )

    def test_scheduling_str(self):
        scheduling = Scheduling.objects.create(
            user=self.user,
            service=self.service,
            barber=self.barber,
            time='17:00-18:00',
            day=date.today(),
            phone='123456789',
        )

        self.assertEqual(str(scheduling), 'jujuba')
