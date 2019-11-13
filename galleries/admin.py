from django.contrib import admin
from django.conf import settings
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.admin import helpers

from .models import Tag, Author, Image, Gallery
from .forms import UploadZipForm

admin.site.register(Tag)
admin.site.register(Author)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'gallery', 'image_thumb')
    list_filter = ('gallery',)
    list_per_page = 20
    readonly_fields = ["image_thumb"]


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'slug', 'main_image',
                    'author', 'created', 'modified')
    list_filter = ['date', 'author', 'tags']
    search_fields = ['title', 'slug']
    readonly_fields = ['image_count', 'slug']
    list_per_page = 20

    def get_urls(self):
        urls = super(GalleryAdmin, self).get_urls()
        custom_urls = [
            path('upload_zip/', self.admin_site.admin_view(self.upload_zip),
                 name='upload_zip')
        ]
        return custom_urls + urls

    def upload_zip(self, request):
        context = {
            'title': "Upload .zip file with photos",
            'site_title': 'Django site admin',
            'site_header': 'Django administration',
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'max_zip_size': settings.MAX_ZIP_FILE_SIZE,
            'has_change_permission': self.has_change_permission(request)
        }

        # Handle form request
        if request.method == 'POST':
            form = UploadZipForm(request.POST, request.FILES)
            if form.is_valid():
                gallery_pk = form.save(request=request)
                return HttpResponseRedirect(reverse('admin:galleries_gallery_change', args=(gallery_pk,)))
        else:
            form = UploadZipForm()
        context['form'] = form
        context['adminform'] = helpers.AdminForm(form,
                                                 list(
                                                     [(None, {'fields': form.base_fields})]),
                                                 {})
        return render(request, 'admin/galleries/upload_zip.html', context)
