from django.shortcuts import render, redirect
from django.urls import reverse
from . import templates
from .models import Event
from mysite.models import *
from datetime import date, datetime, timedelta

# Create your views here.


def index(request):
    if request.user is not None and request.user.username is not "":
        if request.method == "POST":
            slot_date = request.POST.get("slot_date")
            obj = Event.objects.filter(date=slot_date)
            obj.userid = request.user.username
            obj.isBooked = True
            obj.from_time = request.POST.get("start_time")
            obj.to_time = request.POST.get("end_time")

        events = Event.objects.all()  # call all the event objects
        event_count = Event.objects.count()  # counting number of event objects
        i = 0  # counter set to 0
        curr_date = datetime.now().date()  # get today's date
        for event in events:
            if i == event_count:
                break
            # e = event.eventslot.objects.get(id = i)                                             #iterating through the event objects
            e = Eventslot.objects.filter(event=event)
            e = e[0]
            ev_date = e.Date
            delta = curr_date - ev_date
            diff_weeks = delta.days / 7
            if diff_weeks <= 4:
                i += 1
                continue
            else:
                while 1:
                    event.isBooked = True
                    event.user_id = ""
                    new_date = event.date + timedelta(days=84)
                    event.date = new_date
                    event.save()
                    ev_date = event.Date
                    delta = curr_date - ev_date
                    diff_weeks = delta.days / 7
                    if diff_weeks <= 4:
                        i += 1
                        break

        events = Event.objects.all()
        booked_counter = 0  # number of bookings in this month
        user_counter = 0  # number of bookings by this user in this month
        curr_month = curr_date.month  # get current month
        curr_month_events = []
        for event in events:  # get event objects of current month
            e = Eventslot.objects.filter(event=event)
            e = e[0]
            ev_date = e.Date
            event_month = ev_date.month
            if event_month == curr_month:
                curr_month_events.append(event)
        for event in curr_month_events:
            if (
                event.isBooked == True
            ):  # counting the number of booked events this month
                booked_counter += 1
                if (
                    event.user_id == request.user.username
                ):  # counting the number of events booked by this user this month
                    user_counter += 1
        if (
            booked_counter >= 5
        ):  # if number of events in this month exceeds 4, return error
            return render(request, "partyPage/errorA.html", {})
        if user_counter >= 4:
            return render(
                request, "partyPage/errorB.html", {}
            )  # if number of events in this month by this user exceeds 3, return error
        events2 = []
        i = 0
        for event in events:
            if i == event_count:
                break
            e = Eventslot.objects.filter(event=event)
            e = e[0]
            ev_date = e.Date
            delta = curr_date - ev_date
            diff_days = delta.days
            if diff_days < 0:
                if e.event.isBooked == False:
                    events2.append(e)
        context = {"events2": events2, "coord": list(Coordinator.objects.all())}
        return render(request, "partyPage/index.html", context)
    else:
        request.session[
            "next"
        ] = "/partyPage"  # if user is not logged in, redirect to login and then after login bring them back
        return redirect("/login")

    if request.method == "POST":
        return
