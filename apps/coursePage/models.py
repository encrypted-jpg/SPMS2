from django.core.validators import *
from django.db import models


# Create your models here.
class Course(models.Model):
    id = models.IntegerField("id", primary_key=True, blank=False)
    name = models.CharField("name", max_length=20, blank=False)
    num_students = models.IntegerField(
        "num_students", validators=[MaxValueValidator(50)], default=0
    )
    is_active = models.BooleanField("is_active", default="True")
    start_date = models.DateField("start_date", null=True, blank=False)
    last_date = models.DateField("last_date", null=True, blank=False)
    cost = models.IntegerField("cost", null=True, blank=False)
