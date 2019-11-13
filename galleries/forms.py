"""A form to upload zipped file with photos

Raises:
    forms.ValidationError -- BadZipFile - the error raised for bad ZIP files
    forms.ValidationError -- some data in a Zip file (.zip or .zipx) is damaged.
    forms.ValidationError -- if gallery with user typed name already exists
    forms.ValidationError -- if user typed gallery name and chose gallery from the list

Returns:
    on save return gallery id
"""

import logging
import os
import io
import zipfile
import uuid
from datetime import datetime

from django import forms
from django.conf import settings
from django.contrib import messages
from django.utils.text import slugify
from django.core.files.base import ContentFile
from PIL import Image as PILImage

from .models import Author, Gallery, Image, Tag

logger = logging.getLogger(__name__)

all_galleries_folder = os.path.join(settings.BASE_DIR, 'media',
                                    'galleries')
thumbnail_size = 255, 127
web_size = 1023, 800


class UploadZipForm(forms.Form):
    zip_file = forms.FileField()
    title = forms.CharField(max_length=150,
                            required=False,
                            help_text="Type title for the new gallery")
    gallery = forms.ModelChoiceField(Gallery.objects.all(
    ), required=False, help_text='Select gallery to add photos or leave it empty if you are about to create new one')
    date = forms.DateField(widget=forms.SelectDateWidget,
                           help_text='Date of photos', required=False, initial=datetime.now())
    author = forms.ModelChoiceField(Author.objects.all(
    ), required=False, help_text="Select author of the photos")
    tags = forms.ModelMultipleChoiceField(Tag.objects.all(), required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    def clean_zip_file(self):
        zip_file = self.cleaned_data['zip_file']
        try:
            zip = zipfile.ZipFile(zip_file)
        except zipfile.BadZipfile as ex:
            zip.close()
            raise forms.ValidationError(str(ex))

        if zip.testzip():
            zip.close()
            raise forms.ValidationError('File contains errors')

        if zip.fp.size > 1024*1024*settings.MAX_ZIP_FILE_SIZE:
            zip.close()
            raise forms.ValidationError(
                'Size of the file is greater than 50 MB')

        return zip_file

    def clean_title(self):
        title = self.cleaned_data['title']
        if title and Gallery.objects.filter(title=title).exists():
            raise forms.ValidationError(
                f'Gallery {title} already exists.')

        slug = slugify(title)
        if Gallery.objects.filter(slug=slug).exists():
            raise forms.ValidationError(
                f'Gallery with the address: {slug} already exists.')

        return title

    def clean(self):
        cleaned_data = super(UploadZipForm, self).clean()
        title = cleaned_data.get('title')
        gallery = cleaned_data.get('gallery')
        date = cleaned_data.get('date')
        author = cleaned_data.get('author')
        tags = cleaned_data.get('tags')

        if not title and not gallery:
            raise forms.ValidationError(
                'Either choose gallery or type title for a new one')

        if title:
            if not date or not author:
                raise forms.ValidationError(
                    'For new gallery data and author are required')

        return cleaned_data

    def save_images(self, zip_file, gallery):
        gallery_folder = os.path.join(all_galleries_folder, gallery.slug)
        with zipfile.ZipFile(zip_file) as zip:
            for index, filename in enumerate(sorted(zip.namelist())):
                if os.path.dirname(filename):
                    continue

                data = zip.read(filename)
                new_filename = str(uuid.uuid4())
                image_full_path = os.path.join(
                    gallery_folder, f'{new_filename}.jpg')
                thumbnail_full_path = os.path.join(
                    gallery_folder, f'{new_filename}.thumbnail.jpg')
                try:
                    im = PILImage.open(io.BytesIO(data))
                    original_image = im.copy()
                    im.thumbnail(thumbnail_size)
                    im.save(thumbnail_full_path, "JPEG")

                    original_image.thumbnail(web_size)
                    original_image.save(image_full_path, "JPEG")

                    relative_image_path = os.path.join(
                        gallery.slug, f'{new_filename}.jpg')
                    relative_thumbnail_path = os.path.join(
                        gallery.slug, f'{new_filename}.thumbnail.jpg')
                    image = Image(title=filename, gallery=gallery,
                                  image=relative_image_path, thumbnail=relative_thumbnail_path)
                    image.save()
                except IOError as error:
                    logger.error(f'Error on trying to save image: {error}')

    def save(self, request):
        logger.info(f'Gallery Import started: {datetime.now()}')

        gallery = self.cleaned_data['gallery']
        author_id = self.cleaned_data['author']
        zip_file = self.cleaned_data['zip_file']

        if gallery:
            gallery = Gallery.objects.get(pk=gallery.pk)
            self.save_images(zip_file, gallery)
            messages.success(request,
                             'Photos were added to "{0}".'.format(
                                 gallery.title),
                             fail_silently=True)
        else:
            title = self.cleaned_data['title']
            slug = slugify(title)
            gallery = Gallery(
                author=author_id, title=title, description=self.cleaned_data['description'], date=self.cleaned_data['date'], slug=slug)
            gallery.save()
            self.create_folder(gallery.slug)
            self.save_images(zip_file, gallery)
            first_image = Image.objects.filter(gallery=gallery).first()
            gallery.main_image = first_image.thumbnail
            gallery.save()
            messages.success(request,
                             f'Gallery "{gallery.title}" was successfully created.',
                             fail_silently=True)

        logger.info(f'Import finished: {datetime.now()}')
        return gallery.pk

    def create_folder(self, folder_name):
        path = os.path.join(all_galleries_folder, folder_name)
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError as error:
                logger.error(f'Error on creating folder {path}: {error}')
            else:
                logger.info(f'Successfully created folder: {path}')
