from django.shortcuts import render
from .models import Coach


def index(request):
    context = {}
    context['coaches'] = Coach.objects.all()
    return render(request, 'club/index.html', context)
