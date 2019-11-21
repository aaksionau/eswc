from django.shortcuts import render

from .models import GoogleSchedule


def import_schedule(request):
    # TODO: Move configuration to settings
    google_service = GoogleSchedule('https://docs.google.com/spreadsheets/d/1HM9NH4OlTZKtuuNC-CZWWQ_zxPXcaAPFD56hSDRyTNk/edit#gid=0',
                                    'https://www.googleapis.com/auth/spreadsheets.readonly')
    google_service.getdata()
    return render(request, 'club/import_results.html')
