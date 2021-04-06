from django.db import models
from mysite.models import *
from django.core.validators import *


# Create your models here.


class Feedback(models.Model):
    id = models.IntegerField("id", primary_key=True)
    name = models.CharField("name", max_length=50, blank=False)
    text = models.CharField("text", max_length=500, blank=False)
    reply = models.CharField(
        "reply", max_length=500, default="Thanks for your feedback"
    )
    replied = models.BooleanField("replied", default=False)
    user = models.ManyToManyField(NewUser, related_name="user")
    persons = models.ManyToManyField(NewUser, related_name="persons", blank=True)
    date = models.DateField("date", blank=True, null=True)
