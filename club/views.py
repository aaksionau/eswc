
from django.shortcuts import render
from .models import Coach, GoogleSchedule, Schedule

import requests
from decouple import config


def index(request):
    context = {}
    context['coaches'] = Coach.objects.all()
    return render(request, 'club/index.html', context)


def import_schedule(request):
    google_service = GoogleSchedule('https://docs.google.com/spreadsheets/d/1HM9NH4OlTZKtuuNC-CZWWQ_zxPXcaAPFD56hSDRyTNk/edit#gid=0',
                                    'https://www.googleapis.com/auth/spreadsheets.readonly')
    google_service.getdata()
    return render(request, 'club/import_results.html')
