from datetime import datetime

from django.shortcuts import render, render_to_response
from django.contrib import messages
from django.views.generic import FormView

from club.models import Coach, Schedule
from galleries.models import Gallery

from .forms import FeedbackForm
from .models import Feedback

app_name = 'pages'


def index(request):
    context = {}
    context['coaches'] = Coach.objects.all().order_by('order')
    context['schedule_list'] = Schedule.objects.filter(
        date__gte=datetime.now()).filter(type='n').order_by('date')[:10]
    context['tournaments'] = Schedule.objects.filter(
        date__gte=datetime.now()).filter(type='t').order_by('date')[:3]
    context['galleries'] = Gallery.objects.all()[:5]
    return render(request, f'{app_name}/index.html', context)


def donate(request):
    return render(request, f'{app_name}/donate.html')


class FeedbackView(FormView):
    template_name = f'{app_name}/feedback.html'
    form_class = FeedbackForm
    success_url = '/contacts/'

    def form_valid(self, form):
        form.send_email()
        form.save()
        messages.success(
            self.request, 'You successfully sent a message. We will reply soon. Thank you.')
        return super().form_valid(form)


def handler404(request, exception, template_name=f'{app_name}/404.html'):
    response = render_to_response(f'{app_name}/404.html')
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response(f'{app_name}/500.html')
    response.status_code = 500
    return response
