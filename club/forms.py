from django.forms import ModelForm, forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Feedback

from datetime import datetime


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ('created',)

    def send_email(self):
        phone = self.cleaned_data['phone']
        text = self.cleaned_data['text']
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']

        message_to_admin = f'You received message from {name}'
        msg_html = render_to_string(
            'club/email.html', {'phone': phone, 'text': text, 'name': name, 'date': datetime.now().strftime('%x')})

        recipients = settings.FEEDBACK_RECIPIENTS
        send_mail(
            message_to_admin,
            msg_html,
            [email],
            recipients,
            fail_silently=False,
        )
