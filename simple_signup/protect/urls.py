from .views import IndexView, ConTypeView, NotificationList
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from .views import upgrade_me, one_time, ReplyList

urlpatterns = [
    path('', NotificationList.as_view()),
    path('cabinet/', IndexView.as_view()),
    path('not/add/', ConTypeView.as_view()),

    path('login/',
         LoginView.as_view(template_name='protect/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='protect/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='protect/signup.html'),
         name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('onetime/', one_time, name='onetime'),
    path('reply/', ReplyList.as_view()),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
