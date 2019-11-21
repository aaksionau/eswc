from django.conf import settings
from pages.models import Page


def add_menu_pages(request):
    pages = Page.objects.filter(
        published=True, visible_in_menu=True).order_by('order')
    context = {'menu_pages': pages}

    return context
