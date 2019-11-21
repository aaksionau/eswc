from django.conf import settings
from pages.models import Page


def add_menu_pages(request):
    pages = Page.objects.filter(
        published=True, visible_in_menu=True).order_by('order')
    current_path_portions = request.path.split('/')
    current_page = Page.objects.get(slug='home')
    if len(current_path_portions) >= 2 and current_path_portions[1]:
        current_page = Page.objects.filter(
            slug=current_path_portions[1]).first()
    context = {'menu_pages': pages, 'current_page': current_page}

    return context
