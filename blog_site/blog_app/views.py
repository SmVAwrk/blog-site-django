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
        return Posts.objects.filter(is_published=True)
        # .select_realted('category', 'tags')


class Post(DetailView):
    model = Posts
    template_name = 'blog_app/index.html'
    context_object_name = 'post'



def index(request):
    return render(request, 'blog_app/index.html')


def get_category(request, slug):
    return render(request, 'blog_app/category.html')

