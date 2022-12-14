from datetime import datetime

from django.db import models
from django.urls import reverse
from django.contrib.auth import models as models_

from django.db.models import Sum


class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True)


class User(models_.User):
    nameuser_id = models.AutoField(primary_key=True)
    nameuser = models.CharField(max_length=150, unique=True)


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


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.title()


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
