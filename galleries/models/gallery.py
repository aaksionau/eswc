from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError


from .image import Image
from .tag import Tag
from .author import Author
from .audit import Audit


class Gallery(Audit):
    title = models.CharField(max_length=200)
    date = models.DateField()
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    main_image = models.FileField(upload_to='galleries')
    tags = models.ManyToManyField(Tag, related_name='galleries')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def image_count(self):
        return Image.objects.filter(gallery_id=self.pk).count()

    def get_absolute_url(self):
        return reverse('gallery-detail', kwargs={'slug': self.slug})

    def clean(self):
        slug = self.get_slug(self.title)
        if Gallery.objects.filter(slug=slug).exists():
            raise ValidationError(
                f'Gallery with {slug} exist, please change slug or title')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Gallery, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'galleries'
