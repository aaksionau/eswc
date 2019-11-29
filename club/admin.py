from django.contrib import admin
from .models import Coach, Schedule


@admin.register(Coach)
class AdminCoach(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'phone', 'order')


@admin.register(Schedule)
class AdminSchedule(admin.ModelAdmin):
    list_display = ('date', 'type', 'description',
                    'link', 'created', 'updated')
