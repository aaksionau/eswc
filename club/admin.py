from django.contrib import admin
from .models import Coach


@admin.register(Coach)
class AdminCoach(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone',)
