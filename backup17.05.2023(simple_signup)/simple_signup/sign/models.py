from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from django.db import models


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

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
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user


class OneTimeCode(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Content(models.Model):
    """Модель для контента объявления
    --id_notification (IntegerField)
    --contype (CharField)
    --text (TextField)
    --image (ImageField)
    --video(FileField)
    --document(FileField)"""
    id_notification = models.IntegerField()
    contype = models.CharField(max_length=64, default="text")
    text = models.TextField(default="text")
    image = models.ImageField()
    video = models.FileField()
    document = models.FileField()


class Notification(models.Model):
    """Модель для объявлений.  -заголовок(header) -контент(content) -автор(author)
    -дата создания(datetime)"""
    header = models.CharField(max_length=255, default="Default header")
    content = models.ForeignKey(Content.id_notification, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    pass