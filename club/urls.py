from django.apps import apps
from django.urls import path
from .views import *


app_name = apps.get_app_config('club').name

urlpatterns = [
    path('import/', import_schedule, name='import'),
]
