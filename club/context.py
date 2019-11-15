from django.conf import settings


def add_settings(request):
    context = {'analytics_id': settings.GOOGLE_ANALYTICS}

    return context
