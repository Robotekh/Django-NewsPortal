from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.db import models


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

#Кастомизируем форму регистрации SignupForm, которую предоставляет пакет allauth.
#Добавим следующий код в файл, например, sign/models.py.
# В идеале, конечно, скрипты, относящиеся к формам, нужно хранить в отдельном файле forms.py,
# но для нас сейчас это не является принципиальным.


class BasicSignupForm(SignupForm):
    """Модель для формы регистрации"""
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get()
        basic_group.user_set.add(user)
        return user


class OneTimeCode(models.Model):
    """Модель для одноразового кода подтверждения"""
    code = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Content(models.Model):
    """Модель для контента объявления"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_notification = models.IntegerField(null=True)
    contype = models.CharField(max_length=8)
    text = models.TextField(null=True, default='')
    image = models.ImageField(null=True, default='', upload_to='images/')
    video = models.FileField(null=True, default='', upload_to='videos/', verbose_name="")
    file = models.FileField(null=True, default='', upload_to='files/')


class Reply(models.Model):
    """Модель для откликов"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, default='')
    user_name = models.CharField(max_length=100, null=True, default='')
    notification_id = models.CharField(max_length=50, null=True, default='')


class Notification(models.Model):
    """Модель для объявлений."""
    header = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    reply = models.ManyToManyField(Reply, through='NotificationReply')


class NotificationReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)







