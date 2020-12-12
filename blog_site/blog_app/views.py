from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'blog_app/index.html')


def get_category(request, slug):
    return render(request, 'blog_app/category.html')

