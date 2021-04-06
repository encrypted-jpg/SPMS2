from django.core.validators import *
from django.db import models


# Create your models here.
class Competition(models.Model):
    id = models.IntegerField("id", primary_key=True)
    name = models.CharField("name", max_length=100, blank=False)
    from_age = models.IntegerField("from_age", blank=True, null=True)
    to_age = models.IntegerField("to_age", blank=True, null=True)


class Game(models.Model):
    MALE = "Male"
    FEMALE = "Female"
    BOTH = "Both"
    lst = [
        (MALE, "Only Males are allowed"),
        (FEMALE, "Only Females are allowed"),
        (BOTH, "Everybody is allowed"),
    ]
    from_age = models.IntegerField("from_age", blank=False, default=12)
    to_age = models.IntegerField("to_age", blank=False, default=32)
    gender = models.CharField(
        "gender", max_length=10, blank=False, choices=lst, default=BOTH
    )
    game_type = models.CharField("type", max_length=100, blank=False)

    # relationships
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, null=True, blank=True
    )


from mysite.models import NewUser


class Ticket(models.Model):
    num_tickets = models.IntegerField(
        "num_tickets", validators=[MaxValueValidator(4)], default=1
    )
    # relationships
    user = models.ManyToManyField(NewUser)
    competition = models.ManyToManyField(Competition)
