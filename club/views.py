from django.shortcuts import render, render_to_response
from django.contrib import messages
from django.views.generic.edit import FormView

from .models import Coach, GoogleSchedule, Schedule, Feedback
from galleries.models import Gallery
from .forms import FeedbackForm

from datetime import datetime


def index(request):
    context = {}
    context['coaches'] = Coach.objects.all()
    context['schedule_list'] = Schedule.objects.filter(
        date__gte=datetime.now()).filter(type='n').order_by('date')[:10]
    context['tournaments'] = Schedule.objects.filter(
        date__gte=datetime.now()).filter(type='t').order_by('date')[:3]
    context['galleries'] = Gallery.objects.all()[:5]
    return render(request, 'club/index.html', context)


def donate(request):
    return render(request, 'club/donate.html')


def import_schedule(request):
    google_service = GoogleSchedule('https://docs.google.com/spreadsheets/d/1HM9NH4OlTZKtuuNC-CZWWQ_zxPXcaAPFD56hSDRyTNk/edit#gid=0',
                                    'https://www.googleapis.com/auth/spreadsheets.readonly')
    google_service.getdata()
    return render(request, 'club/import_results.html')


class FeedbackView(FormView):
    template_name = 'club/feedback.html'
    form_class = FeedbackForm
    success_url = '/contacts/'

    def form_valid(self, form):
        form.send_email()
        form.save()
        messages.success(
            self.request, 'You successfully sent a message. We will reply soon. Thank you.')
        return super().form_valid(form)


def handler404(request, exception, template_name='pages/404.html'):
    response = render_to_response('club/404.html')
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('club/500.html')
    response.status_code = 500
    return response
