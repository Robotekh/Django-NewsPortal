import random

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from sign.models import OneTimeCode

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        context['onetime_code'] = not OneTimeCode.objects.filter(user=self.request.user.id).exists()
        return context


# def usual_login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         OneTimeCode.objects.create(code=random.choice('abcde'), user=user)
#
#         send_mail(
#             "Код подтверждения",
#             f"Введите ваш код подтверждения: {random.choice('abcde')}",
#             "svetlakov.dmtry@yandex.ru",
#             ["svetlakov.dmtry@yandex.ru"],
#             fail_silently=False,
#         )
#         # redirect somewhere
#     else:
#         # return an 'invalid login' error message
#
# def login_with_code_view(request):
#     username = request.POST['username']
#     code = request.POST['code']
#     if OneTimeCode.objects.filter(code=code, user__username=username).exists():
#         login(request, user)
#     else:
#         # error

# def usual_login_view(request):
#     print('!!!!!!!!!')
#     print(request.user)
#     username = request.GET['username']
#     password = request.GET['password']
#     user = authenticate(request, username=username, password=password)
#     code = '0000'
#     if user is not None:
#         OneTimeCode.objects.create(code=code, user=user)
#         send_mail(
#                     "Код подтверждения",
#                     f"Введите ваш код подтверждения: {code}",
#                     "svetlakov.dmtry@yandex.ru",
#                     ["svetlakov.dmtry@yandex.ru"],
#                     fail_silently=False,
#                 )






    #user.email_user('login with one-time code', text)
