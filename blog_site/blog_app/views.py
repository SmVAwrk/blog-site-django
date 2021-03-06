from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import F, Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from slugify import slugify

from .forms import *

from blog_app.models import *


class Home(ListView):
    """
    Представление-класс для главной страницы.
    Передает только опубликованные и незакрепленные посты, а также название страницы.
    """
    template_name = 'blog_app/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

    def get_queryset(self):
        return Posts.objects.filter(is_published=True, on_main=False).select_related('author')


class PostsByCategory(ListView):
    """
    Представление-класс для просмотра постов определенной категории.
    Передает опубликованные посты из данной категории,
    а также название страницы, как название категории.
    """
    template_name = 'blog_app/category.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Categories.objects.get(slug=self.kwargs['slug']).title
        return context

    def get_queryset(self):
        return Posts.objects.filter(is_published=True, category__slug=self.kwargs['slug']).select_related('author')


class PostsByTag(ListView):
    """
    Представление-класс для просмотра постов, связанных с определенным тегом.
    Передает опубликованные посты с данным тегом, а также название страницы, как название тега.
    """
    template_name = 'blog_app/category.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тег: ' + Tags.objects.get(slug=self.kwargs['slug']).title
        return context

    def get_queryset(self):
        return Posts.objects.filter(is_published=True, tags__slug=self.kwargs['slug']).select_related('author')


class GetPost(DetailView):
    """Представление-класс для просмотра конкретного поста."""
    model = Posts
    template_name = 'blog_app/single.html'
    context_object_name = 'post_item'

    def get_context_data(self, **kwargs):
        """Метод добавления формы и комментариев к контексту, а также увеличения кол-ва просмотров."""
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        context['form'] = AddCommentForm()
        context['comments'] = Comments.objects.filter(post=self.object.pk).select_related('author')
        return context

    def post(self, request, *args, **kwargs):
        """
        Метод для обработки формы комментариев.
        При добавление комментария полю author присваивается user запроса.
        """
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = self.get_object()
            new_comment.save()
            messages.success(request, 'Ваш комментарий успешно добавлен!')
            return redirect('post', self.kwargs['slug'])
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        messages.error(request, 'Не удалось добавить комментарий.')
        return render(request, self.template_name, context)


class Search(ListView):
    """
    Представление-класс для просмотра постов которые ищет пользователь.
    Передает опубликованные посты, у которых в названии или контенте содержится введенная пользователем строка.
    Также передает саму введенную строку и название страницы.
    """
    template_name = 'blog_app/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Posts.objects.filter(
            Q(is_published=True) &
            (Q(title__icontains=self.request.GET.get("s")) |
             Q(content__icontains=self.request.GET.get("s")))
        ).select_related('author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Поиск по "{self.request.GET.get("s")}"'
        context['s'] = f's={self.request.GET.get("s")}&'
        return context


def registration(request):
    """
    Представление-функция для регистрации пользователей на сайте.
    Передает и обрабатывает форму регистрации.
    Также передает название страницы.
    """
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже зарегистрированы.')
        return redirect('home')
    title = 'Регистрация'
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        messages.error(request, 'При регистрации произошла ошибка.')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog_app/registration.html', {'form': form, 'title': title})


def user_login(request):
    """
    Представление-функция для авторизации пользователей на сайте.
    Передает и обрабатывает форму авторизации.
    Также передает название страницы.
    """
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже авторизованы.')
        return redirect('home')
    title = 'Вход'
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        messages.error(request, 'Не удалось войти в аккакунт.')
    else:
        form = UserLoginForm()
    return render(request, 'blog_app/registration.html', {'form': form, 'title': title})


def user_logout(request):
    """Представление-функция для деавторизации пользователей на сайте."""
    logout(request)
    return redirect('login')


def add_post(request):
    """
    Представление-функция для добавления поста на сайте.
    Передает и обрабатывает форму добавления поста.
    При добавление поста:
    полю author присваивается user запроса,
    поле slug автоматически создается на основе поля title.
    Также передает название страницы.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    title = 'Добавление записи'
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.slug = slugify(new_post.title)
            new_post.save()
            messages.success(request, 'Ваш пост был успешно добавлен!')
            return redirect('home')
        messages.error(request, 'Не удалось добавить пост.')
    else:
        form = AddPostForm()
    return render(request, 'blog_app/add_post.html', {'title': title, 'form': form})


