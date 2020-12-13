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


class Post(DetailView):
    model = Posts
    template_name = 'blog_app/index.html'
    context_object_name = 'post_item'





def get_category(request, slug):
    return render(request, 'blog_app/category.html')

