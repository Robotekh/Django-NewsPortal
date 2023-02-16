from django.urls import path, re_path
# Импортируем созданное нами представление
from .views import AppointmentView

urlpatterns = [
    path('make_appointment/', AppointmentView.as_view())
]
