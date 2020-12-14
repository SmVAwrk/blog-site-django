from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

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
        return Posts.objects.filter(is_published=True, on_main=False).select_related('category', 'author')


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
        return Posts.objects.filter(is_published=True, category__slug=self.kwargs['slug']).select_related('category',
                                                                                                          'author')


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
        return Posts.objects.filter(is_published=True, tags__slug=self.kwargs['slug']).select_related('category',
                                                                                                      'author')


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

