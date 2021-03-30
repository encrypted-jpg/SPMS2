from django.db import models
from mysite.models import NewUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here


class Membership_form(models.Model):
    id = models.IntegerField("id", primary_key=True)
    user = models.OneToOneField(
        NewUser, on_delete=models.CASCADE, null=True, blank=False
    )
    ACardNum = models.CharField("aCardNum", max_length=20, default="", null=True)
    num_months = models.PositiveIntegerField("num_months", default=1, null=True)
    cert = models.FileField("cert", null=True, blank=True)
    is_approved = models.BooleanField(
        "is_approved", null=True, blank=True, default=True
    )
    phone_num = PhoneNumberField("phone_num", null=True, blank=True)
    reason = models.CharField(
        "reason", max_length=150, default="", null=True, blank=True
    )
    removed = models.BooleanField("removed", null=True, blank=True, default=False)
