from django.urls import path
from . import views

app_name = 'galleries'

urlpatterns = [
    path('', views.GalleriesListView.as_view(), name='list'),
    path('<slug:slug>/', views.GalleryDetailView.as_view(), name='detail'),
    path('archive/<int:year>/',
         views.GalleriesArchiveListView.as_view(), name='archive'),
    path('filter/tag/<int:tag>/',
         views.GalleriesFilterByTagListView.as_view(), name='filter-tag'),
    path('filter/author/<int:author>/',
         views.GalleriesFilterByAuthorListView.as_view(), name='filter-author'),
]
