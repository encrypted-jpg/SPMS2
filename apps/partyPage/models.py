from django.core.validators import *

from mysite.models import *


# Create your models here.


class Event(models.Model):
    userid = models.CharField("userid", max_length=50, blank=True, null=True)
    isBooked = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)


class EventBooking(models.Model):
    user_aadhar = models.IntegerField("acard_num", default=0, null=True, blank=True)
    Date = models.DateField("date", blank=False)
    from_time = models.TimeField("from_time", blank=False)
    to_time = models.TimeField("to_time", blank=False)
