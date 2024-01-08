from django.test import TestCase, Client
from .models import Services, Scheduling
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse


class ServicesModelTestCase(TestCase):

    def test_create_service(self):
        service = Services.objects.create(
            name='Corte Degradê',
            price=18.0,
        )

        service_bd = Services.objects.get(id=service.id)

        self.assertEqual(service_bd.name, 'Corte Degradê')
        self.assertEqual(service_bd.price, 18.0)


user_instance = User.objects.get(username='ericj')
service_instance = Services.objects.get(name='Corte Degradê')


class ServiceHomeViewTestCase(TestCase):

    def test_home_view(self):
        client = Client()

        url = reverse('home')

        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class ServiceCreateViewTestCase(TestCase):

    def test_create_service_view(self):
        client = Client()

        url = reverse('create_service')

        response = client.post(url, {'name': 'Sobrancelha', 'price': 5})

        # objects_previous = Services.objects.count()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Services.objects.count(), 1)
