from django.contrib import admin
from django.db import models

from .models import Portfolio, PortfolioCategory, BlogPost, BlogCategory, Profile
from mdeditor.widgets import MDEditorWidget


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'filter')
    search_fields = ['title']


admin.site.register(PortfolioCategory)
admin.site.register(Portfolio, PortfolioAdmin)


class BlogPostAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


admin.site.register(BlogCategory)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Profile)