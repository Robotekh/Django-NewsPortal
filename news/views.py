# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from typing import Dict, Any

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .tasks import send_notifications


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    queryset = Post.objects.order_by(  # сортировка по имени
        "-time_in"
    )
    # ordering = 'title' #Узнать для чего
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 15  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному посту
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'post'


# Добавляем новое представление для создания постов.
class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель постов
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    # проверка есть ли права у пользователя на данные действия
    permission_required = ('news.add_post')

    def form_valid(self, form):
        # Нужно для обработки запроса
        post = form.save(commit=False)
        # Достаёт параметр type из пути запроса и записывает его в поле type в бд
        post.type = self.request.path.split('/')[1]
        return super().form_valid(form)

    # #Функция для вызова задачи в celery
    # def get(self, request):
    #     printer.apply_async([10], countdown = 5) #10-аргумент countdown задержка в секундах
    #     hello.delay()
    #     return HttpResponse('Hello!')

# Добавил миксин LoginRequiredMixin для проверки аунтефикации
class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    # проверка есть ли права у пользователя на данные действия
    permission_required = ('news.change_post')

    # login_url адрес перенапрвления если пользователь не аутентифицирован
    #login_url = '/login/'

    def form_valid(self, form):
        # Нужно для обработки запроса
        post = form.save(commit=False)
        # Достаёт параметр type из пути запроса и записывает его в поле type в бд
        post.type = self.request.path.split('/')[1]
        return super().form_valid(form)

    # Сначала мы должны каким-то образом передать в шаблон страницы информацию о
    # том, есть ли пользователь в группе Premium
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


# class ProtectedView(LoginRequiredMixin, TemplateView):
#     template_name = 'prodected_page.html'

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category_name = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category_name).order_by('-time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category_name.subscribers.all()
        context['category'] = self.category_name
        return context

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news/')

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категорий'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
