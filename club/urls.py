from django.urls import path
from .views import *

app_name = 'club'

urlpatterns = [
    path('', index, name='main'),
]
