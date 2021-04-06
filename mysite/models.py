from django.db import models
from django.contrib.auth.models import (
    User,
    Group,
    Permission,
    UserManager,
    AbstractUser,
)
from django.utils.translation import gettext_lazy as _
from apps.compPage.models import *
from apps.coursePage.models import Course
from apps.partyPage.models import *
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here
class MemberslotManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, *kwargs).filter(type=Slot.Types.MEMBERSLOT)


class CompslotManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, *kwargs).filter(type=Slot.Types.COMPSLOT)


class GameslotManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, *kwargs).filter(type=Slot.Types.GAMESLOT)


class CourseslotManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, *kwargs).filter(type=Slot.Types.COURSESLOT)


class EventslotManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, *kwargs).filter(type=Slot.Types.EVENTSLOT)


class NewUser(User):
    class Types(models.TextChoices):
        MEMBER = "MEMBER", "Member"
        COORDINATOR = "COORDINATOR", "Coordinator"
        COMMITTEE = "COMMITTEE", "Committee"
        MANAGER = "MANAGER", "Manager"

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=Types.MEMBER
    )
    age = models.DateField("age", blank=False)
    gender = models.CharField("gender", max_length=10, blank=False)
    city = models.CharField(
        "city", max_length=15, default="Kharagpur", null=True, blank=True
    )
    country = models.CharField(
        "country", max_length=15, default="India", null=True, blank=True
    )
    phone_num = PhoneNumberField(
        "phone_num", null=True, blank=True
    )  # Need to add Unique is True
    pincode = models.IntegerField("pincode", null=True, blank=True)
    address = models.CharField("address", null=True, max_length=200, blank=True)
    membership_date = models.DateField("membership_date", default="2001-01-01")
    aCardNum = models.IntegerField(
        "acard_num", default=0, null=True, blank=True
    )  # aadhar number
    comp_participated = models.IntegerField("comp_participated", default=0, blank=False)
    is_member = models.BooleanField("is_member", default="False")
    is_coordinator = models.BooleanField("is_coordinator", default="False")
    is_committee = models.BooleanField("is_committee", default="False")
    course_last_date = models.DateField("course_last_date", default="2001-01-01")

    # relationships
    event = models.OneToOneField(
        Event, on_delete=models.SET_NULL, null=True, blank=True
    )
    course = models.ManyToManyField(Course, blank=True)
    cert = models.FileField("cert", blank=True, null=True)
    comp_cert = models.FileField("comp_cert", blank=True, null=True)
    course_count = models.IntegerField("course_count", default=0, null=True, blank=True)
    comp_count = models.IntegerField("course_count", default=0, null=True, blank=True)
    event_count = models.IntegerField("course_count", default=0, null=True, blank=True)


class Slot(models.Model):
    class Types(models.TextChoices):
        MEMBERSLOT = "MEMBERSLOT", "Memberslot"  # Slot for Swimming
        COMPSLOT = "COMPSLOT", "Compslot"
        GAMESLOT = "GAMESLOT", "Gameslot"
        COURSESLOT = "COURSESLOT", "Courseslot"
        EVENTSLOT = "EVENTSLOT", "Eventslot"

    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=Types.MEMBERSLOT
    )
    MALE = "Male"
    FEMALE = "Female"
    BOTH = "Both"
    lst = [
        (MALE, "Only Males are allowed"),
        (FEMALE, "Only Females are allowed"),
        (BOTH, "Everybody is allowed"),
    ]
    gender = models.CharField(
        "gender", max_length=10, blank=False, choices=lst, default=BOTH
    )
    from_time = models.TimeField("from_time", max_length=10, blank=False)
    to_time = models.TimeField("to_time", max_length=10, blank=False)
    Date = models.DateField("date", max_length=20, blank=False)
    Day = models.CharField("day", max_length=20, null=True, blank=True, default="")
    rem_num_participants = models.IntegerField("rem_num_participants", default=50)
    max_num_participants = models.IntegerField("max_num_participants", default=50)
    # relationships
    # from compPage models.py
    competition = models.OneToOneField(
        Competition, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    game = models.OneToOneField(Game, on_delete=models.SET_NULL, null=True, blank=True)

    # from coursePage models.py
    course = models.ManyToManyField(Course, blank=True)

    # from partyPage.models
    event = models.OneToOneField(
        Event, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )

    # to store users for games mainly
    users = models.ManyToManyField(NewUser, blank=True)

    # functions
    def setDay(self, Date):
        lst = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        Day = lst[datetime.strptime(str(Date), "%Y-%m-%d").weekday()]
        return Day


class Memberslot(Slot):
    objects = MemberslotManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Slot.Types.MEMBERSLOT
        return super().save(*args, **kwargs)


class Compslot(Slot):
    objects = CompslotManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Slot.Types.COMPSLOT
        return super().save(*args, **kwargs)


class Gameslot(Slot):
    objects = GameslotManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Slot.Types.GAMESLOT
        return super().save(*args, **kwargs)


class Courseslot(Slot):
    objects = CourseslotManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Slot.Types.COURSESLOT
        return super().save(*args, **kwargs)


class Eventslot(Slot):
    objects = EventslotManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = Slot.Types.EVENTSLOT
        return super().save(*args, **kwargs)


class NonMemberManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, *kwargs).filter(type=NewUser.Types.NON_MEMBER)
        )


class MemberManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, *kwargs).filter(type=NewUser.Types.MEMBER)


class CoordinatorManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, *kwargs).filter(type=NewUser.Types.COORDINATOR)
        )


class CommitteeManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, *kwargs).filter(type=NewUser.Types.COMMITTEE)


class ManagerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, *kwargs).filter(type=NewUser.Types.MANAGER)


class Member(NewUser):
    objects = MemberManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = NewUser.Types.MEMBER
        return super().save(*args, **kwargs)


class Coordinator(NewUser):
    is_coordinator = True
    objects = CoordinatorManager()
    is_staff = True

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = NewUser.Types.COORDINATOR
        return super().save(*args, **kwargs)


class Committee(NewUser):
    is_committee = True
    objects = CommitteeManager()
    is_staff = True

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = NewUser.Types.COMMITTEE
        return super().save(*args, **kwargs)


class Manager(NewUser):
    is_superuser = True
    is_staff = True
    objects = ManagerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = NewUser.Types.MANAGER
        return super().save(*args, **kwargs)


class Message(models.Model):
    head = models.CharField(max_length=30, default="", blank=True, null=True)
    Description = models.CharField(max_length=100, default="", blank=True, null=True)
    users = models.ManyToManyField(NewUser)
    Date = models.DateField("Date", blank=False, default="2001-01-01")
    url = models.URLField(default="#", blank=True, null=True)
