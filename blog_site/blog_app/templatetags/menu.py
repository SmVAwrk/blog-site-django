from django import template
from blog_app.models import *
from django.db.models import *

register = template.Library()


@register.inclusion_tag('blog_app/menu_tpl.html')
def show_menu(menu_class='menu', request=None):
    """
    Кастомный тег для вывода футера и хедера
    :param menu_class: аргумент, определяющий класс меню тега "div" в шаблоне
    :param request: для передачи данных о запросе пользователя
    """
    categories = Categories.objects.annotate(cnt=Count('posts')).filter(cnt__gt=0)
    return {'categories': categories, 'menu_class': menu_class, 'request': request}

