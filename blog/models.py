from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.shortcuts import reverse


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.FileField(
        upload_to='blogposts', blank=True, null=True)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')

    objects = models.Manager()
    published_objects = BlogPostManager()

    class Meta:
        ordering = ['created', ]

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.title = self.title.title()
        self.modified = timezone.now()
        self.slug = slugify(self.title)
        if self.published and not self.published_date:
            self.published_date = timezone.now()
        return super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f"BlogPost('{self.title}', '{self.slug}')"
