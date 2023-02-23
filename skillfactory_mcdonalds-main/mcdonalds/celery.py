import os
from celery import Celery
from celery.schedules import crontab


 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcdonalds.settings')
 
app = Celery('mcdonalds')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

#В качестве более реального, пусть и абсолютно бесполезного,
# примера посмотрим, как можно запустить счётчик от 1 до N как периодическую задачу.
# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'board.tasks.printer',
#         'schedule': 5,
#         'args': (5,),
#     },
# }

#Например, чтобы выполнить какую-то задачу каждый понедельник в 8 утра, необходимо
# в расписание добавить следующее:

# app.conf.beat_schedule = {
#     'action_every_monday_8am': {
#         'task': 'action',
#         'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#         'args': (agrs),
#     },
# }

app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'task': 'board.tasks.clear_old',
        'schedule': crontab(),
    },
}