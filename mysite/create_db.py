import datetime
from faker import Faker
from random import randint, choice


def setDay(Date):
    lst = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    Day = lst[datetime.datetime.strptime(str(Date), "%Y-%m-%d").weekday()]
    return Day


def cslots():
    ptd = datetime.date(2021, 4, 5)
    i = 0
    while i != 7:
        td = ptd + datetime.timedelta(days=i)
        if not setDay(td) in ["Saturday", "Sunday"]:
            s = Slot(
                from_time="6:00:00",
                to_time="7:00:00",
                Date=td,
                Day=setDay(td),
                gender="Male",
            )
            s.save()
            s = Slot(
                from_time="7:00:00",
                to_time="8:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
            s = Slot(
                from_time="8:00:00",
                to_time="9:00:00",
                Date=td,
                Day=setDay(td),
                gender="Female",
            )
            s.save()
            s = Slot(
                from_time="15:00:00",
                to_time="16:00:00",
                Date=td,
                Day=setDay(td),
                gender="Male",
            )
            s.save()
            s = Slot(
                from_time="16:00:00",
                to_time="17:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
            s = Slot(
                from_time="17:00:00",
                to_time="18:00:00",
                Date=td,
                Day=setDay(td),
                gender="Female",
            )
            s.save()
            s = Slot(
                from_time="20:00:00",
                to_time="21:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
            s = Slot(
                from_time="21:00:00",
                to_time="22:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
            s = Courseslot(
                from_time="6:00:00",
                to_time="7:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
            s = Courseslot(
                from_time="8:00:00",
                to_time="9:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
            s = Courseslot(
                from_time="15:00:00",
                to_time="16:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
            s = Courseslot(
                from_time="17:00:00",
                to_time="18:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
        else:
            s = Slot(
                from_time="6:00:00",
                to_time="7:00:00",
                Date=td,
                Day=setDay(td),
                gender="Male",
            )
            s.save()
            s = Slot(
                from_time="7:00:00",
                to_time="8:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
            s = Slot(
                from_time="8:00:00",
                to_time="9:00:00",
                Date=td,
                Day=setDay(td),
                gender="Female",
            )
            s.save()
            s = Courseslot(
                from_time="6:00:00",
                to_time="7:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
            s = Courseslot(
                from_time="8:00:00",
                to_time="9:00:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
        i += 1


cslots()


def eslots():
    td = datetime.date(2021, 3, 13)
    i = 0
    while i != 24:
        td += datetime.timedelta(days=1)
        if setDay(td) in ["Saturday", "Sunday"]:
            s = Eventslot(
                from_time="18:00:00",
                to_time="22:30:00",
                Date=td,
                Day=setDay(td),
            )
            s.save()
            i += 1


eslots()


def eobj():
    for x in Eventslot.objects.all():
        e = Event(userid=None)
        e.save()
        x.event = e
        x.save()


eobj()
