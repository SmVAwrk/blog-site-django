from django import template
from blog_app.models import *
from django.db.models import *

register = template.Library()


@register.inclusion_tag('blog_app/menu_tpl.html')
def show_menu(menu_class='menu', request=None):
    categories = Categories.objects.annotate(cnt=Count('posts')).filter(cnt__gt=0)
    return {'categories': categories, 'menu_class': menu_class, 'request': request}

