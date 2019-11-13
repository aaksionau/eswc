from django.contrib import admin
from .models import Coach, Schedule, Feedback


@admin.register(Coach)
class AdminCoach(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone',)


@admin.register(Schedule)
class AdminSchedule(admin.ModelAdmin):
    list_display = ('date', 'type', 'description',
                    'link', 'created', 'updated')


@admin.register(Feedback)
class AdminFeedback(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'text', 'created')
