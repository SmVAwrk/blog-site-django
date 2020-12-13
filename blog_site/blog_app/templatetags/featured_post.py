from django import template

from blog_app.models import Posts

register = template.Library()


@register.inclusion_tag('blog_app/featured_post_tpl.html')
def get_main_posts():
    main_posts = Posts.objects.filter(on_main=True)
    return {'main_posts': main_posts}
