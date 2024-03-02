from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from twilio.rest import Client
from .models import Scheduling


@receiver(post_save, sender=Scheduling)
def send_sms_notification(sender, instance, created, **kwargs):
    if created:
        account_sid = 'AC233045d1f5ec5ed0a82cedb7e2f281bf'
        auth_token = '40fd3e810cd740f81a2ca3ba7417c914'
        twilio_phone_number = '+12015847819'

        client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body='Muito Obrigado por confiar no nossos serviços\n' +
            'A Barbearia Boa Vista agredece!\n' +
            f'Serviço: {instance.service}\n Dia: {instance.day}\n Horário: {instance.get_time_display()}',
            from_=twilio_phone_number,
            to='+55' + instance.phone,
        )

    except Exception as e:
        print(f'Erro ao enviar mensagem{str(e)}')
        
