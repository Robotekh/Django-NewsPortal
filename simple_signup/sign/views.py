import random

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from .models import OneTimeCode


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

@login_required
def upgrade_me(request):
    user = request.user
    code = random.randint(0000, 9999)
    OneTimeCode.objects.all().delete()
    if user.email is not None:
        OneTimeCode.objects.create(code=code, user=user)
        send_mail(
            "Код подтверждения",
            f"Введите в окошке на сайте ваш код подтверждения: {code}",
            user.email,
            [user.email],
            fail_silently=False,
        )
    # premium_group = Group.objects.get(name='premium')
    # if not request.user.groups.filter(name='premium').exists():
    #     premium_group.user_set.add(user)
    return redirect('/')

@login_required
def one_time(request):
    username = request.user.username
    code = request.POST.get('onetime')
    user = request.user
    print(username)
    if OneTimeCode.objects.filter(user=request.user.id).exists():
        if OneTimeCode.objects.filter(user=request.user.id)[0].code == code:
            premium_group = Group.objects.get(name='premium')
            if not request.user.groups.filter(name='premium').exists():
                premium_group.user_set.add(user)
        else:
            #Вывысти сообщение код не верный
            pass
    OneTimeCode.objects.all().delete()
    return redirect('/')