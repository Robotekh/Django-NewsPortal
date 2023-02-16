import django_filters
from news.forms_wigets.widget import MyDateInput
from .models import Post


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author_name = django_filters.CharFilter(lookup_expr='icontains')
    # Реализация поля ввода даты с использованием собственного виджета который использует стандартный DateInput
    release_year__gt = django_filters.DateFilter(field_name='time_in', lookup_expr='date__gt', widget=MyDateInput)

    model = Post
    fields = ['title', 'author_name', 'release_year__gt']
    # Реализация техже фильтров только через мета класс как в курсе
    # class Meta:
    #     # В Meta классе мы должны указать Django модель,
    #     # в которой будем фильтровать записи.
    #     model = Post
    #     # В fields мы описываем по каким полям модели
    #     # будет производиться фильтрация.
    #     fields = {
    #         # поиск по названию
    #         'title': ['icontains'],
    #         'author_name': ['icontains'],
    #         # количество товаров должно быть больше или равно
    #         'time_in': ['date__gt'],
    #     }
