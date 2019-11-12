from django.db import models
from django.core.validators import RegexValidator


class Coach(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12,
                             validators=[RegexValidator(regex='^\([0-9]{3}\)[0-9]{3}-[0-9]{4}$')])
    email = models.EmailField()

    avatar = models.FileField(upload_to='coaches/', blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Coach("{self.name}", "{self.phone}", "{self.email}")'

    class Meta:
        ordering = ['name']
