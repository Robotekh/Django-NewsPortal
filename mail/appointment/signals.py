from django.db.models.signals import post_save, post_delete#Для отправки по сигналу (событию) сохранения в модель appointment
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Appointment

# создаём функцию-обработчик с параметрами под регистрацию сигнала
# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Appointment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )
    print(f'!!!!!!!!{instance.client_name} {instance.date.strftime("%d %m %Y")}')

# коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
# post_save.connect(notify_managers_appointment, sender=Appointment)

@receiver(post_delete, sender=Appointment)
def notify_managers_appointment_canceled(sender, instance, **kwargs):
    subject = f'{instance.client_name} has canceled his appointment!'
    mail_managers(
        subject=subject,
        message=f'Canceled appointment for {instance.date.strftime("%d %m %Y")}',
    )

    print(subject)