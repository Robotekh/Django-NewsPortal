from django.contrib import admin
from .models import Content, Notification, OneTimeCode, Reply, NotificationReply

admin.site.register(Content)
admin.site.register(Notification)
admin.site.register(OneTimeCode)
admin.site.register(Reply)
admin.site.register(NotificationReply)