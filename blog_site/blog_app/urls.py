from django.urls import path, include

from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('post/<str:slug>/', Post.as_view(), name='post'),
    path('tags/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
    path('registration/', registration, name='reg'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
