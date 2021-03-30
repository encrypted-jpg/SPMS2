from django.db import models
from django.core.validators import *


# Create your models here.
class Course(models.Model):
    name = models.CharField("name", max_length=20, blank=False)
    num_students = models.IntegerField(
        "num_students", validators=[MaxValueValidator(50)], default=0
    )
    is_active = models.BooleanField("is_active", default="False")
    start_date = models.DateField("start_date", null=True, blank=False)
    last_date = models.DateField("last_date", null=True, blank=False)
    min_age = models.IntegerField("min_age", default=10, null=True, blank=False)
    max_age = models.IntegerField("max_age", default=25, null=True, blank=False)
