from django.contrib.sitemaps import Sitemap
from .models import Post, Portfolio


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.all().filter(status=1)

    def lastmod(self, obj):
        return obj.updated_on


class PortfolioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Portfolio.objects.all()

    def lastmod(self, obj):
        return obj.updated_on