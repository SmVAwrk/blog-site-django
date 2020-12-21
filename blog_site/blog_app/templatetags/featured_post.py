from django import template

from blog_app.models import Posts

register = template.Library()


@register.inclusion_tag('blog_app/featured_post_tpl.html')
def get_main_posts():
    """Кастомный тег для вывода закрепелнных и опубликованных постов на главной странице"""
    main_posts = Posts.objects.filter(is_published=True, on_main=True).select_related('author')
    return {'main_posts': main_posts}

