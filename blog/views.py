from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import BlogPost


class BlogPostsListView(ListView):
    model = BlogPost
    paginate_by = 10
    context_object_name = 'blogposts'
    queryset = BlogPost.published_objects.order_by('created')


class BlogPostDetailView(DetailView):
    model = BlogPost
    context_object_name = 'post'
    queryset = BlogPost.published_objects.all()
