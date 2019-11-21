from django.urls import path
from .views import FeedbackView, index, donate

app_name = 'pages'

urlpatterns = [
    path('home/', index, name='home'),
    path('', index, name='home-default'),
    path('contacts/', FeedbackView.as_view(), name='contacts'),
    path('donate/', donate, name='donate'),
]
