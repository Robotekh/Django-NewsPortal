from django.contrib import admin
from .models import Post, PostCategory, Category, MyModel
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

# Регистрируем модели для перевода в админке
class CategoryAdmin(TranslationAdmin):
    model = Category


class MyModelAdmin(TranslationAdmin):
    model = MyModel

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(MyModel)
admin.site.register(Category)
