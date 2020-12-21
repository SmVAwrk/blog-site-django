from django import template
from django.db.models import Count, Sum

from blog_app.models import Posts, Tags

register = template.Library()


@register.inclusion_tag('blog_app/sidebar_tpl.html')
def get_sidebar_data(cnt=3):
    """
    Кастомный тег для вывода последних постов,
    популярных постов и тегов(в порядке популярности) на сайдбар
    :param cnt: кол-во выводимых постов
    """
    recent = Posts.objects.filter(is_published=True).order_by('-created_at')[:cnt].select_related('author')
    popular = Posts.objects.filter(is_published=True).order_by('-views')[:cnt].select_related('author')
    tags = Tags.objects.annotate(sum=Sum('posts__views')).order_by('-sum')
    return {'recent': recent, 'popular': popular, 'tags': tags}





