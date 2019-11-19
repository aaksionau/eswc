from django.urls import path
from . import views

app_name = 'galleries'

urlpatterns = [
    path('', views.GalleriesListView.as_view(), name='list'),
    path('<slug:slug>/', views.GalleryDetailView.as_view(), name='detail'),
    path('archive/<int:year>/',
         views.GalleriesArchiveListView.as_view(), name='archive')
]
