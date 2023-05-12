from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth import models as models_
from django.contrib.auth.models import User


from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.db.models import Sum

from django.core.cache import cache

from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy # импортируем «ленивый» геттекст с подсказкой


class Category(models.Model):
    # добавим переводящийся текст подсказку к полю (help_text)
    category_name = models.CharField(max_length=150, help_text=_('category name'), unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.category_name


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0, db_column='rating')

    @property
    def update_rating(self):
        return self._rating

    @update_rating.setter
    def update_rating(self, value):
        self._rating = value if value >= 0 else 0
        self.save()



class Post(models.Model):
    news = 'N'
    article = 'A'
    position = [(news, 'Новость'), (article, 'Статья')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    author_name = models.TextField(max_length=150)
    type = models.CharField(max_length=1, choices=position, default='news')
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=150, default="Title")
    text = models.TextField(default='Post text')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...' if len(self.text) > 124 else self.text + '...'

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
        #return f'/news/{self.id}'

    #Функция для перезаприси кэширования при сохранении объекта
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post_list-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его
        cache.delete(f'post_detail-{self.pk}')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        # Изначально был return self.name.title()
        # Работает кроме админки self.category
        return self.category.__str__()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='Coment text')
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

# переопределить класс формы так, чтобы при успешном
# прохождении регистрации добавлять присоединение к базовой группе пользователей.
#Кастомизируем форму регистрации SignupForm, которую предоставляет пакет allauth.
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='kinds',
        verbose_name=pgettext_lazy('help text for MyModel model', 'This is the help text'),
    )