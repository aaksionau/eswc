from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify
from django.shortcuts import reverse
from django.core.validators import RegexValidator


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    parent = models.ForeignKey(
        'Page', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True)
    visible_in_menu = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.slug = slugify(self.title)

        if self.published and not self.published_date:
            self.published_date = datetime.now()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def get_absolute_url(self):
        return reverse('page-detail', kwargs={'slug': self.slug})


class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=14,
                             validators=[RegexValidator(regex='^\([0-9]{3}\)[0-9]{3}-([0-9]){4}$')], help_text="Enter phone in the following format (111)111-1111")
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-created']
