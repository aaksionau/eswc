from django.contrib import admin
from .models import BlogPost

from django_summernote.admin import SummernoteModelAdmin


@admin.register(BlogPost)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'published',
                    'created', 'updated', 'author')
    list_filter = ('author',)
    list_per_page = 20
