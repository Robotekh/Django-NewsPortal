from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


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
        basic_group = Group.objects.get()
        basic_group.user_set.add(user)
        return user