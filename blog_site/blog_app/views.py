from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F, Q
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .forms import *

from blog_app.models import *


class Home(ListView):
    model = Posts
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
    model = Posts
    template_name = 'blog_app/category.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Categories.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Posts.objects.filter(is_published=True, category__slug=self.kwargs['slug']).select_related('author')


class PostsByTag(ListView):
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


class Post(DetailView):
    model = Posts
    template_name = 'blog_app/single.html'
    context_object_name = 'post_item'

    def get_context_data(self, **kwargs):
        """Увеличение кол-ва просмотров"""
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class Search(ListView):
    template_name = 'blog_app/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Posts.objects.filter(Q(title__icontains=self.request.GET.get("s")) |
                                    Q(content__icontains=self.request.GET.get("s"))).select_related('author')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Поиск по "{self.request.GET.get("s")}"'
        context['s'] = f's={self.request.GET.get("s")}&'
        return context


def registration(request):
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
    logout(request)
    return redirect('login')


def add_post(request):
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





