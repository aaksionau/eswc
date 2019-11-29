import os
from datetime import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Coach(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=14,
                             validators=[RegexValidator(regex='^\([0-9]{3}\)[0-9]{3}(-[0-9]{2}){2}|$')], help_text="Enter phone in the following format (111)111-11-11")
    email = models.EmailField()
    order = models.IntegerField(blank=True, null=True)
    avatar = models.FileField(upload_to='coaches/', blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Coach("{self.name}", "{self.phone}", "{self.email}")'

    class Meta:
        ordering = ['order']


SCHEDULE_TYPES = (
    ('p', 'Practice'),
    ('n', 'No practice'),
    ('t', 'Tournament'),
)


class Schedule(models.Model):
    date = models.DateField(unique=True)
    type = models.CharField(
        max_length=1, choices=SCHEDULE_TYPES, default='p')
    cover_image = models.FileField(upload_to='tournaments/')
    link = models.URLField()
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.date}'


class GoogleSchedule:
    def __init__(self, url, scope):
        self.url = url
        self.scope = [scope]
        self.data = None

    def _get_type(self, value):
        if value.find('TOURNAMENT') > -1:
            return 't'
        elif value.find('NO PRACTICE') > -1:
            return 'n'
        else:
            return 'p'

    def getdata(self):
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials

        path_to_cred = os.path.join(settings.BASE_DIR, 'credentials.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            path_to_cred, self.scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        sheet = client.open_by_url(self.url).sheet1

        data = sheet.get_all_records()
        for index, item in enumerate(data):
            if index == 0:
                continue
            try:
                date = datetime.strptime(
                    item[' Date'], '%x')
                type = self._get_type(item['Event'])
                link = description = ''
                if type == 'n':
                    description = item['Event'].replace(
                        'NO PRACTICE - ', '').capitalize()
                elif type == 't':
                    if item['New Shot Taught']:
                        value = sheet.cell(
                            index+2, 3, value_render_option='FORMULA').value.lstrip('=HYPERLINK(').rstrip(')')
                        link, description = value.split(',')

                schedule, _ = Schedule.objects.get_or_create(
                    date=date)
                schedule.type = type
                schedule.link = link.strip('"')
                schedule.description = description.strip('"')
                schedule.save()

            except TypeError as err:
                logger.error(f'{datetime.now}: Type error: {err}')
            except ValueError as err:
                logger.error(f'{datetime.now}: Value error: {err}')
