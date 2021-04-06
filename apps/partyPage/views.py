from django.shortcuts import render, redirect
from django.urls import reverse
from . import templates
from .models import Event, EventBooking
from mysite.models import *
from datetime import date, datetime, timedelta
from django.contrib import messages


# Create your views here.


def index(request):
    if request.user is not None and request.user.username is not "":
        USER = NewUser.objects.get(username=request.user.username)
        if request.method == "POST":
            slot_date = request.POST.get("slot_date")  # Get Slot date
            slot_date = date.strftime(
                datetime.strptime(slot_date, "%B %d, %Y"), "%Y-%m-%d"
            )  # Convert slot date into req format of yyyy-mm-dd
            # ATTENTION!!!!This is the message to be displayed if the user has selected a slot for this month and there are already 5 bookings in this month
            events = Event.objects.all()
            booked_counter = 0
            slot_date = datetime.strptime(slot_date, '%Y-%m-%d')
            slot_date = datetime.date(slot_date)
            emonth = slot_date.month  # Get month of slot date
            curr_month_events = []
            for event_ in events:  # get event objects of current month
                e = Slot.objects.get(type=Slot.Types.EVENTSLOT, event=event_)
                ev_date = e.Date
                event_month = ev_date.month
                if event_month == emonth:
                    curr_month_events.append(event_)
            for event in curr_month_events:
                if (
                        event.isBooked == True
                ):  # counting the number of booked events this month
                    booked_counter += 1
            if booked_counter == 5:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Sorry, we are already booked fully for this month!!",
                    extra_tags="custom",
                )
                return redirect("/userPortal/event/")
            # show the above error message after redirecting to partyPage itself. I have added an if else statement.
            else:
                event_slot = Slot.objects.get(type=Slot.Types.EVENTSLOT, Date=slot_date)
                obj = event_slot.event
                obj.userid = request.user.username
                obj.isBooked = True
                event_slot.from_time = request.POST.get("start_time")
                event_slot.to_time = request.POST.get("end_time")
                USER = NewUser.objects.get(username=request.user.username)
                if USER.aCardNum == 0:
                    USER.aCardNum = request.POST.get("aadhar_number")
                if USER.phone_num == 0000000000 or USER.phone_num is None:
                    USER.phone_num = request.POST.get("phone_number")
                obj2 = EventBooking()
                obj2.user_aadhar = USER.aCardNum
                obj2.Date = slot_date
                obj2.from_time = request.POST.get("start_time")
                obj2.to_time = request.POST.get("end_time")
                obj.save()
                obj2.save()
                USER.save()
            return redirect("/partyPage/register?date=" + str(slot_date))

        comp = Compslot.objects.all()
        events = Event.objects.all()  # call all the event objects
        event_count = Event.objects.count()  # counting number of event objects
        i = 0  # counter set to 0
        curr_date = datetime.now().date()  # get today's date
        for event in events:
            if i == event_count:
                break
            # e = event.eventslot.objects.get(id = i)    #iterating through the event objects
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
                    event.isBooked = False
                    event.user_id = ""
                    e = Eventslot.objects.filter(event=event)
                    e = e[0]
                    new_date = e.Date + timedelta(days=84)
                    e.Date = new_date
                    event.save()
                    e.save()
                    ev_date = e.Date
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
        for event_ in events:  # get event objects of current month
            e = Slot.objects.get(type=Slot.Types.EVENTSLOT, event=event_)
            ev_date = e.Date
            event_month = ev_date.month
            if event_month == curr_month:
                curr_month_events.append(event_)
        for event in curr_month_events:
            if (
                    event.isBooked == True
            ):  # counting the number of booked events this month
                booked_counter += 1
                if (
                        event.userid == request.user.username and event.is_paid == True
                ):  # counting the number of events booked by this user this month
                    user_counter += 1
        events2 = []
        i = 0
        for event_ in events:
            if i == event_count:
                break
            e = Slot.objects.get(type=Slot.Types.EVENTSLOT, event=event_)
            ev_date = e.Date
            c_count = Compslot.objects.filter(Date=ev_date).count()
            if c_count != 0:
                continue
            delta = curr_date - ev_date
            diff_days = delta.days
            if diff_days < 0:
                if not e.event.is_paid:
                    events2.append(e)

        # ATTENTION!!! This is the message to be displayed if the user has already booked 3 parties, i.e, user_counter = 3
        if user_counter == 3:
            messages.add_message(
                request,
                messages.INFO,
                "You have already booked 3 parties for the next 60 days!! Limit reached.",
                extra_tags="custom",
            )
            return redirect("/userPortal/event/")

        context = {
            "events2": events2,
            "committee": list(Committee.objects.all()),
            "booked_counter": booked_counter,
            "user_counter": user_counter,
            "USER": USER,
            "messages": messages.get_messages(request),
        }
        return render(request, "partyPage/index.html", context)
    else:
        request.session[
            "next"
        ] = "/partyPage"  # if user is not logged in, redirect to login and then after login bring them back
        return redirect("/login")


def payment(request):
    if request.user is not None and request.user.username is not "":
        USER = NewUser.objects.get(username=request.user.username)
        if request.GET.get("date") is not None and request.GET.get("done") is "1":
            slot_date = date.strftime(
                datetime.strptime(request.GET.get("date"), "%Y-%m-%d"), "%Y-%m-%d"
            )
            e = Eventslot.objects.get(Date=slot_date)
            e = e.event
            e.is_paid = True
            e.save()
            USER.event_count += 1
            USER.save()

            # This is the message to be displayed for successful booking
            messages.add_message(
                request,
                messages.INFO,
                "Your booking is successful!!",
                extra_tags="custom",
            )
            return redirect("/userPortal/event/")
        eb = EventBooking.objects.filter(user_aadhar=USER.aCardNum, Date=request.GET.get("date"))[0]
        td = datetime(1, 1, 1, eb.to_time.hour, eb.to_time.minute, eb.to_time.second) - datetime(1, 1, 1,
                                                                                                 eb.from_time.hour,
                                                                                                 eb.from_time.minute,
                                                                                                 eb.from_time.second)
        k = td.seconds / 3600
        p = round(k)
        if p < k:
            p += 1
        dat = request.GET.get("date")
        context = {
            "date": dat,
            "cost": 10000 * p
        }
        return render(request, "partyPage/register.html", context)
    else:
        request.session[
            "next"
        ] = "/partyPage"  # if user is not logged in, redirect to login and then after login bring them back
        return redirect("/login")
