from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Page, Feedback


@admin.register(Page)
class AdminPage(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'order', 'parent',
                    'visible_in_menu', 'created', 'published')
    list_filter = ('parent',)


@admin.register(Feedback)
class AdminFeedback(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'text', 'created')
