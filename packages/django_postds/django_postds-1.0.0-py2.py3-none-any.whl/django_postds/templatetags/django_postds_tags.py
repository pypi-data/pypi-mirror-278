from django.template import Library, loader
from ..models import Portfolio, PortfolioCategory, BlogPost
from _data import postds


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


c = postds.context


@register.simple_tag
def portfolio():
    t = loader.get_template(c["template_name"] + '/' + c['filenames']['_portfolio'])
    c.update({
        'categories': PortfolioCategory.objects,
        'items': Portfolio.objects,
    })
    return t.render(c)


@register.simple_tag
def recent_blog_posts():
    t = loader.get_template(c["template_name"] + '/' + c['filenames']['_recent_blog_posts'])
    objects = BlogPost.objects.filter(status=1).filter(remarkable=True).order_by('-updated_on')
    c.update({
        'top3': objects[:3],
    })
    return t.render(c)