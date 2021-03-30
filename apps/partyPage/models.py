from django.db import models
from mysite.models import *
from django.core.validators import *

# Create your models here.


class Event(models.Model):
    name = models.CharField("name", max_length=50, blank=False)
    is_approved = models.BooleanField(default=False)
