from django.db import models

from .audit import Audit


class Author(Audit):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)

    objects = models.Manager()

    def __str__(self):
        return self.last_name + ' ' + self.first_name
