from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', BlogPostsListView.as_view(), name='list'),
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='detail'),
]
