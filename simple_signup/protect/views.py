
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .models import Content, Notification
from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import random
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm, OneTimeCode, NotificationReply, Reply
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver


# создаём функцию-обработчик сигнала создания отклика
@receiver(post_save, sender=Reply)
def notify_managers_appointment(sender, instance, created, **kwargs):
    notific = Notification.objects.get(id=instance.notification_id)
    send_mail(
        "Новый отклик",
        f"По вашему объявлению есть новый отклик от пользователя: {instance.user_name}. \
        Отклик в объявлении: {notific.header[:20]}...  от: {notific.datetime}",
        notific.author.email,
        [notific.author.email],
        fail_silently=False,
    )


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
    return redirect('/cabinet/')


# для проверки одноразового кода и добавления в группу премиум
@login_required
def one_time(request):
    code = request.POST.get('onetime')
    user = request.user
    if OneTimeCode.objects.filter(user=request.user.id).exists():
        if OneTimeCode.objects.filter(user=request.user.id)[0].code == code:
            premium_group = Group.objects.get()
            if not request.user.groups.filter(name='premium').exists():
                premium_group.user_set.add(user)
        else:
            #Вывысти сообщение код не верный
            pass
    OneTimeCode.objects.all().delete()
    return redirect('/cabinet/')


# для личного кабинета
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        context['onetime_code'] = not OneTimeCode.objects.filter(user=self.request.user.id).exists()
        return context


# Создание объявления (выпадающий список)
class ConTypeView(LoginRequiredMixin, CreateView):
    model = Content
    template_name = 'protect/contype.html'
    success_url = 'not/add'

    def get(self, request, **kwargs):
        context = {
            # фильтруем контент по текущему пользователю и контент которому не присвоен id объявления
            'cont': Content.objects.filter(user_id=request.user.id).filter(id_notification=None),
            'check_title': False,
        }
        return HttpResponse(render(request, 'protect/contype.html', context))

    def post(self, request, **kwargs):
        req = request.POST
        # если нажата кнопка удалить
        if 'but2' in req:
            # проходим по запросу
            for requ in req:
                # обновляем их содержимое текстов в бд(Content)
                if 'ident' in requ:
                    obj = Content.objects.get(id=requ[5:])
                    obj.text = req[requ]
                    obj.save()
                    del obj
            #print(req)
            # удаляем элемент
            Content.objects.get(id=req['but2']).delete()
            context = {
                # фильтруем контент по текущему пользователю и контент которому не присвоен id объявления
                'cont': Content.objects.filter(user_id=request.user.id).filter(id_notification=None),
                'titl': req['titl']
            }
            return HttpResponse(render(request, 'protect/contype.html', context))
        if 'dellimage' in req:
            obj = Content.objects.get(id=req['dellimage'])
            obj.delete()
            obj.save()
            del obj
        if 'dellfile' in req:
            obj = Content.objects.get(id=req['dellfile'])
            obj.delete()
            obj.save()
            del obj
        if 'dellvideo' in req:
            obj = Content.objects.get(id=req['dellvideo'])
            obj.delete()
            obj.save()
            del obj
        # если нажата кнопка but
        if 'add' in req:
            # обновляем их содержимое текстов в бд(Content)
            #print(req)
            for requ in req:
                if 'ident' in requ:
                    obj = Content.objects.get(id=requ[5:])
                    obj.text = req[requ]
                    print(req[requ])
                    obj.save()
                    del obj
            # если нажата кнопка добавить
            if req['add'] == 'add':
                # если выбрано добавить текст
                if req['spisok'] == 'текст':
                    # создаём объект текст
                    Content.objects.create(user=request.user, contype='текст')
                # если выбрано добавить картинку
                if req['spisok'] == 'картинка':
                    # создаём объект картинка
                    Content.objects.create(user=request.user, contype='картинка')
                if req['spisok'] == 'файл':
                    # создаём объект файл
                    Content.objects.create(user=request.user, contype='файл')
                if req['spisok'] == 'видео':
                    # создаём объект картинка
                    Content.objects.create(user=request.user, contype='видео')
                context = {
                    # фильтруем контент по текущему пользователю и контент которому не присвоен id объявления
                    'cont': Content.objects.filter(user_id=request.user.id).filter(id_notification=None),
                    'titl': req['titl']
                }
                return HttpResponse(render(request, 'protect/contype.html', context))
        # если нажата кнопка создать объявление
        if 'create_not' in req:
            # если нажата кнопка создать объявление
            if req['create_not'] == 'create':
                if 'titl' in req:
                    # если пустой заголовок
                    if req['titl'] == '':
                        # возвращаем форму с пометкой пустой заголовок
                        context = {
                            # фильтруем контент по текущему пользователю и контент которому не присвоен id объявления
                            'cont': Content.objects.filter(user_id=request.user.id).filter(id_notification=None),
                            'check_title': True,
                        }
                        return HttpResponse(render(request, 'protect/contype.html', context))
                    else:
                        for requ in req:
                            if 'ident' in requ:
                                obj = Content.objects.get(id=requ[5:])
                                obj.text = req[requ]
                                print(req[requ])
                                obj.save()
                                del obj
                        # если заголовок не пустой создаём объект объявление (Notification)
                        notif = Notification.objects.create(header=req['titl'], author_id=request.user.id)
                        # фильтруем контент по текущему пользователю
                        cont = Content.objects.filter(user_id=request.user.id)
                        for i in cont:
                            print(i)
                            # каждому элементу присваиваем id толькочто созданного эл-та
                            if i.id_notification is None:
                                i.id_notification = notif.id
                                i.save()
                        context = {
                            # фильтруем контент по текущему пользователю и контент которому не присвоен id объявления
                            'cont': Content.objects.filter(user_id=request.user.id).filter(id_notification=None),
                            'titl': req['titl']
                        }
                        return HttpResponse(render(request, 'protect/contype.html', context))
        # если нажата кнопка добавить картинку
        if 'addimage' in req:
            if request.FILES:
                obj = Content.objects.get(id=req['addimage'])
                obj.image = request.FILES['image'+req['addimage']]
                obj.save()
                del obj
        # если нажата кнопка добавить файл
        if 'addfile' in req:
            if request.FILES:
                obj = Content.objects.get(id=req['addfile'])
                obj.file = request.FILES['file'+req['addfile']]
                obj.save()
                del obj
        # если нажата кнопка добавить документ
        if 'addvideo' in req:
            if request.FILES:
                obj = Content.objects.get(id=req['addvideo'])
                obj.video = request.FILES['video' + req['addvideo']]
                obj.save()
                del obj
        return redirect('/not/add')


class NotificationList(LoginRequiredMixin, CreateView):
    model = Notification
    template_name = 'protect/notification_list.html'
    success_url = '/'

    def get(self, request, **kwargs):
        context = {
            # фильтруем контент по текущему пользователю и контент которому не присвоен id объявления
            'cont': Content.objects.filter(id_notification__isnull=False),
            'nots': Notification.objects.all(),
            'notreply': NotificationReply.objects.all(),
            'reply': Reply.objects.all(),
            'is_not_premium': not self.request.user.groups.filter(name='premium').exists(),
        }
        return HttpResponse(render(request, 'protect/notification_list.html', context))

    def post(self, request, **kwargs):
        if 'create_reply' in request.POST:
            if 'reply' in request.POST:
                repl = Reply.objects.create(user_id=request.user, text=request.POST['reply'],
                                            notification_id=request.POST['create_reply'],
                                            user_name=request.user.username)
                notif = Notification.objects.get(id=request.POST['create_reply'])
                NotificationReply.objects.create(reply=repl, notification=notif)
        context = {
            # фильтруем контент по текущему пользователю и контент которому не присвоен id объявления
            'cont': Content.objects.filter(id_notification__isnull=False),
            'nots': Notification.objects.all(),
            'notreply': NotificationReply.objects.all(),
            'reply': Reply.objects.all(),
            'is_not_premium': not self.request.user.groups.filter(name='premium').exists(),
        }
        return HttpResponse(render(request, 'protect/notification_list.html', context))


class ReplyList(LoginRequiredMixin, CreateView):
    model = Reply
    template_name = 'protect/reply_list.html'
    success_url = '/'

    def get(self, request, **kwargs):
        context = {
            # фильтруем контент по текущему пользователю и контент которому не присвоен id объявления
            'nots': Notification.objects.filter(author_id=request.user.id),
            'notreply': NotificationReply.objects.all(),
            'reply': Reply.objects.all(),
            'is_not_premium': not self.request.user.groups.filter(name='premium').exists(),
        }
        return HttpResponse(render(request, 'protect/reply_list.html', context))

    def post(self, request, **kwargs):
        if 'delete_reply' in request.POST:
            if Reply.objects.filter(id=request.POST['delete_reply']).exists():
                Reply.objects.get(id=request.POST['delete_reply']).delete()

        if 'accept_reply' in request.POST:
            if Reply.objects.filter(id=request.POST['accept_reply']).exists():
                user = Reply.objects.get(id=request.POST['accept_reply']).user_id
                text = Reply.objects.get(id=request.POST['accept_reply']).text
                send_mail(
                    "Ваш отклик принял пользователь",
                    f"Ваш отклик: {text[:50]}...  принял пользователь: {user}",
                    user.email,
                    [user.email],
                    fail_silently=False,
                )

        context = {
            # фильтруем контент по текущему пользователю и контент которому не присвоен id объявления
            'nots': Notification.objects.filter(author_id=request.user.id),
            'notreply': NotificationReply.objects.all(),
            'reply': Reply.objects.all(),
            'is_not_premium': not self.request.user.groups.filter(name='premium').exists(),
        }
        return HttpResponse(render(request, 'protect/reply_list.html', context))


