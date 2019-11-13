from django.urls import path
from .views import *

app_name = 'club'

urlpatterns = [
    path('', index, name='main'),
    path('contacts/', FeedbackView.as_view(), name='contacts'),
    path('import/', import_schedule, name='import'),
]
