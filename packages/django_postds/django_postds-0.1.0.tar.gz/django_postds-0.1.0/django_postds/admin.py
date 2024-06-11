from django.contrib import admin
from django.db import models

from .models import Portfolio, PortfolioCategory, Post, PostCategory, Profile
from mdeditor.widgets import MDEditorWidget


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'filter')
    search_fields = ['title']


admin.site.register(PortfolioCategory)
admin.site.register(Portfolio, PortfolioAdmin)


class PostAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


admin.site.register(PostCategory)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile)