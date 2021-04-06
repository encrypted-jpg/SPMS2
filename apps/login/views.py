from datetime import timedelta, datetime, date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from mysite.models import *


# Create your views here.


def index(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request, username=username, password=password
        )  # Checks for User Authentication with given credentials
        if user is not None:
            login(request, user)
            update_status(username)
            try:
                if request.session[
                    "next"
                ]:  # Redirects to a Page if it's value is set in request.session["next"]
                    url = request.session["next"]
                    del request.session["next"]
                    return redirect(url)
            except:
                return redirect("/userPortal/")
        else:  # Displays a message if the Authentication is Failed
            messages.add_message(
                request, messages.INFO, "Username or Password is incorrect!!"
            )
    if request.user is not None and request.user.username is not "":
        update_status(request.user.username)
        try:
            if request.session["next"]:
                url = request.session["next"]
                del request.session["next"]
                return redirect(url)
        except:
            return redirect("/userPortal/")
    context = {
        "messages": messages.get_messages(request),
    }
    return render(request, "login/index.html", context)


def logoutPage(request):  # Logouts the User
    logout(request)
    return redirect("/")


def update_status(
    username,
):  # Updating the User Status when ever the user logs in with the current date
    user = NewUser.objects.get(username=username)
    # iterating over all the slots to set day
    for set_day_slot in Slot.objects.all():
        set_day_slot.Day = set_day_slot.setDay(set_day_slot.Date)
        set_day_slot.save()

    # shifting slots
    slots_ordering = Memberslot.objects.all()
    slots_course = Courseslot.objects.all()
    slots_ordering = list(slots_ordering) + list(slots_course)
    curr_date = datetime.now().date()
    Day = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
    mon_date = curr_date - timedelta(days=Day)
    for Slots in slots_ordering:
        while Slots.Date < mon_date:
            Slots.Date = Slots.Date + timedelta(days=7)
            Slots.save()
    curr = date.today()
    if (
        curr > user.course_last_date and user.type == "MEMBER"
    ):  # if the course last date has been reached
        crs = user.course.all()
        for cr in crs:
            for x in Courseslot.objects.filter(
                course=cr
            ):  # Remove user from all courseslots
                x.users.remove(user)
                x.save()
        user.course_last_date = date(2001, 1, 1)  # default the course_last_date
        user.course.clear()
        user.save()
    if curr > user.membership_date and user.type == "MEMBER":  # Checking for membership
        user.membership_date = date(2001, 1, 1)
        user.save()
    for x in Compslot.objects.all():
        m = Message.objects.filter(head="Swimming Slot Cancelled", Date=x.Date)
        if len(m) > 0:
            m = m[0]
        else:
            continue
        if len(m.users.all()) > 0:
            pass
        else:
            lst = []
            for y in Memberslot.objects.filter(Date=x.Date):
                for z in y.users.all():
                    lst.append(z)
                y.users.clear()
                y.rem_num_participants = 50
                y.save()
            for x in lst:
                m.users.add(x)
            m.save()
    for x in Courseslot.objects.all():
        m = Message.objects.filter(head="Course Slot Cancelled", Date=x.Date)
        if len(m) > 0:
            m = m[0]
        else:
            continue
        if len(m.users.all()) > 0:
            pass
        else:
            lst = []
            for y in Courseslot.objects.filter(Date=x.Date):
                for z in y.users.all():
                    lst.append(z)
                y.users.clear()
                y.rem_num_participants = 50
                y.save()
            for x in lst:
                m.users.add(x)
            m.save()
