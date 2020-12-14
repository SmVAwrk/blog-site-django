from django.urls import path, include

from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('post/<str:slug>/', Post.as_view(), name='post'),
    path('tags/<str:slug>/', PostsByTag.as_view(), name='tag'),

]
