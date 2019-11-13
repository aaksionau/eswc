from django.db import models
from django.utils.html import mark_safe
from django.dispatch import receiver
from django.conf import settings
import os

from .audit import Audit


def gallery_upload_path(instance, filename):
    return f'galleries/{instance.gallery.slug}/{filename}'


def gallery_upload_path_for_small(instance, filename):
    return f'galleries/{instance.gallery.slug}/small/{filename}'


class Image(Audit):
    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to=gallery_upload_path_for_small)
    image = models.FileField(upload_to=gallery_upload_path)
    gallery = models.ForeignKey(
        'Gallery', on_delete=models.CASCADE, related_name='images')

    objects = models.Manager()

    def image_thumb(self):
        return mark_safe(f'<img src="/media/galleries/{self.thumbnail}" width="100"/>')

    image_thumb.allow_tags = True

    def __str__(self):
        return self.image.name


@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    all_galleries_folder = os.path.join(settings.BASE_DIR, 'media',
                                        'galleries')
    if instance.image:
        path = os.path.join(all_galleries_folder, instance.image.path)
        if os.path.isfile(path):
            os.remove(path)

    if instance.thumbnail:
        path = os.path.join(all_galleries_folder, instance.thumbnail.path)
        if os.path.isfile(path):
            os.remove(path)
