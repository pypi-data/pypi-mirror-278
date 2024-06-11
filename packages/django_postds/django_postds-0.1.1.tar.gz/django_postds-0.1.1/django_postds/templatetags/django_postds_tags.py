from django.template import Library, loader
from ..models import Portfolio, PortfolioCategory, Post
from _data import postds


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


template_name = postds.active_template


@register.simple_tag(takes_context=True)
def portfolio(context):
    t = loader.get_template(template_name + '/' + postds.context['filenames']['_portfolio'])
    context.update({
        'template_name': template_name,
        'categories': PortfolioCategory.objects,
        'items': Portfolio.objects,
    })
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def recent_blog_posts(context):
    t = loader.get_template(template_name + '/' + postds.context['filenames']['_recent_blog_posts'])
    objects = Post.objects.filter(status=1).filter(remarkable=True).order_by('-updated_on')
    context.update({
        'template_name': template_name,
        'top3': objects[:3],
    })
    return t.render(context.flatten())