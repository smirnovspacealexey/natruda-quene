from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import models
import datetime


class Log(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    logg = models.TextField(blank=True, null=True)
    datetime = models.DateTimeField('дата, время', default=timezone.now)

    @staticmethod
    def add_new(logg, name=None):
        Log.objects.create(name=name, logg=logg)

    def __str__(self):
        return f'{self.name} - {self.datetime}'

