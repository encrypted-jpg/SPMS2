from django.db import models
from mysite.models import *
from django.core.validators import *

# Create your models here.


class Event(models.Model):
    name = models.CharField("name", max_length=50, blank=False)
    is_approved = models.BooleanField(default=False)


class EventBooking(models.Model):
    user_aadhar = models.IntegerField("acard_num", default=0, null=True, blank=True)
    Date = models.DateField("date", blank=False)
    from_time = models.TimeField("from_time", blank=False)
    to_time = models.TimeField("to_time", blank=False)
