from django.shortcuts import render
from django.contrib import messages
from django.views.generic.edit import FormView

from .models import Coach, GoogleSchedule, Schedule, Feedback
from .forms import FeedbackForm


def index(request):
    context = {}
    context['coaches'] = Coach.objects.all()
    return render(request, 'club/index.html', context)


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
