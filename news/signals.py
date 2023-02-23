from django.db.models.signals import m2m_changed
from django.dispatch import receiver


from news.models import PostCategory
from .tasks import send_notifications


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        #Создаём задачу отправки сообщения в celery в файле tasks.py
        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)