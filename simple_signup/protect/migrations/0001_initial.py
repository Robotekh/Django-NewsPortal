# Generated by Django 4.2 on 2023-05-26 02:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='', null=True)),
                ('user_name', models.CharField(default='', max_length=100, null=True)),
                ('notification_id', models.CharField(default='', max_length=50, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OneTimeCode',
            fields=[
                ('code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protect.notification')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protect.reply')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='reply',
            field=models.ManyToManyField(through='protect.NotificationReply', to='protect.reply'),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_notification', models.IntegerField(null=True)),
                ('contype', models.CharField(max_length=8)),
                ('text', models.TextField(default='', null=True)),
                ('image', models.ImageField(default='', null=True, upload_to='images/')),
                ('video', models.FileField(default='', null=True, upload_to='videos/', verbose_name='')),
                ('file', models.FileField(default='', null=True, upload_to='files/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
