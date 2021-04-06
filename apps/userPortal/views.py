from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from . import templates
from mysite.models import *
from apps.coursePage.models import Course
from apps.partyPage.models import *
from .forms import UploadFileForm
from apps.suggestionPortal.models import *
from .models import Membership_form
from datetime import datetime, timedelta, date
import os


# Create your views here.


def index(request):
    return redirect("/userPortal/availableSlots/")


def availableSlots(request):
    # shifting swimming and course slots by one week
    slots_ordering = Memberslot.objects.all()
    slots_course = Courseslot.objects.all()
    slots_ordering = list(slots_ordering) + list(slots_course)
    curr_date = datetime.now().date()
    Day = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
    mon_date = curr_date - timedelta(days=Day + 1)
    for Slots in slots_ordering:
        while Slots.Date < mon_date:
            Slots.Date = Slots.Date + timedelta(days=7)
            Slots.save()

    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        if str(USER.membership_date) == "2001-01-01" and USER.type == "MEMBER":
            return redirect("/userPortal/registrationPage/")
        if request.GET.get("add") is "0":
            SLOT = Memberslot.objects.get(id=request.GET.get("id"))
            SLOT.rem_num_participants = SLOT.rem_num_participants + 1
            SLOT.users.remove(USER)
        elif request.GET.get("add") is "1":
            swimming_slots2 = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
            if swimming_slots2.count() is 5:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Limit of 5 Swimming slots reached",
                    extra_tags="custom",
                )
            else:
                SLOT = Memberslot.objects.get(id=request.GET.get("id"))
                SLOT.rem_num_participants = SLOT.rem_num_participants - 1
                SLOT.users.add(USER)
                SLOT.save()
        if USER.gender == "Male":
            monday_slots = (
                Memberslot.objects.filter(Day="Monday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Female")
            )
            tuesday_slots = (
                Memberslot.objects.filter(Day="Tuesday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Female")
            )
            wednesday_slots = (
                Memberslot.objects.filter(Day="Wednesday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Female")
            )
            thursday_slots = (
                Memberslot.objects.filter(Day="Thursday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Female")
            )
            saturday_slots = (
                Memberslot.objects.filter(Day="Saturday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Female")
            )
            friday_slots = (
                Memberslot.objects.filter(Day="Friday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Female")
            )
            sunday_slots = (
                Memberslot.objects.filter(Day="Sunday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Female")
            )
        if USER.gender == "Female":
            monday_slots = (
                Memberslot.objects.filter(Day="Monday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Male")
            )
            tuesday_slots = (
                Memberslot.objects.filter(Day="Tuesday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Male")
            )
            wednesday_slots = (
                Memberslot.objects.filter(Day="Wednesday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Male")
            )
            thursday_slots = (
                Memberslot.objects.filter(Day="Thursday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Male")
            )
            saturday_slots = (
                Memberslot.objects.filter(Day="Saturday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Male")
            )
            friday_slots = (
                Memberslot.objects.filter(Day="Friday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Male")
            )
            sunday_slots = (
                Memberslot.objects.filter(Day="Sunday")
                .exclude(rem_num_participants="0")
                .exclude(gender="Male")
            )
        slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        for idx in slots:
            monday_slots = monday_slots.exclude(id=idx.id)
            tuesday_slots = tuesday_slots.exclude(id=idx.id)
            wednesday_slots = wednesday_slots.exclude(id=idx.id)
            thursday_slots = thursday_slots.exclude(id=idx.id)
            friday_slots = friday_slots.exclude(id=idx.id)
            saturday_slots = saturday_slots.exclude(id=idx.id)
            sunday_slots = sunday_slots.exclude(id=idx.id)

        monday_count = monday_slots.count()
        tuesday_count = tuesday_slots.count()
        wednesday_count = wednesday_slots.count()
        thursday_count = thursday_slots.count()
        friday_count = friday_slots.count()
        saturday_count = saturday_slots.count()
        sunday_count = sunday_slots.count()

        for comp_booked in Competition.objects.all():
            SLOTS = Memberslot.objects.filter(Date=comp_booked.slot.Date)
            if SLOTS.count() > 0:
                SLOTS = SLOTS[0]
                if SLOTS.Day == "Monday":
                    monday_slots = []
                    monday_count = 0
                if SLOTS.Day == "Tuesday":
                    tuesday_slots = []
                    tuesday_count = 0
                if SLOTS.Day == "Wednesday":
                    wednesday_slots = []
                    wednesday_count = 0
                if SLOTS.Day == "Thursday":
                    thursday_slots = []
                    thursday_count = 0
                if SLOTS.Day == "Friday":
                    friday_slots = []
                    friday_count = 0
                if SLOTS.Day == "Saturday":
                    saturday_slots = []
                    saturday_count = 0
                if SLOTS.Day == "Sunday":
                    sunday_slots = []
                    sunday_count = 0
        context = {
            "slots": slots,
            "monday_slots": monday_slots,
            "tuesday_slots": tuesday_slots,
            "wednesday_slots": wednesday_slots,
            "thursday_slots": thursday_slots,
            "friday_slots": friday_slots,
            "saturday_slots": saturday_slots,
            "sunday_slots": sunday_slots,
            "monday_count": monday_count,
            "tuesday_count": tuesday_count,
            "wednesday_count": wednesday_count,
            "thursday_count": thursday_count,
            "friday_count": friday_count,
            "saturday_count": saturday_count,
            "sunday_count": sunday_count,
            "messages": messages.get_messages(request),
            "USER": USER,
            "msgs": msgs,
            "swimming_slots": swimming_slots2,
            "swimming_slots_count": swimming_slots_count,
            "course_slots": course_slots2,
            "course_slots_count": course_slots_count,
            "game_slots": game_slots2,
            "game_slots_count": game_slots_count,
            "bookings_count": bookings_count,
            "upcoming_bookings": bookings2,
            "messages": messages.get_messages(request),
            "messages_object": messages_object2,
            "messages_object_count": messages_object_count,
        }
        return render(request, "userPortal/availableSlots.html", context)
    else:
        return redirect("/login")


def registrationPage(request):
    if request.user is not None and request.user.username is not "":
        User = NewUser.objects.get(username=request.user.username)
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        if not str(User.membership_date) == "2001-01-01":
            m = Membership_form.objects.filter(user=User)
            # Is a Member display expiration data/ option for extension
            if request.POST.get("num_months") is not None:
                num = request.POST.get("num_months")
                User.membership_date = datetime.strptime(
                    str(User.membership_date), "%Y-%m-%d"
                )
                User.membership_date += timedelta(days=int(num) * 30)
                User.membership_date = (
                    User.membership_date.date()
                )  # Increment in Membership Date
                User.save()
                messages.add_message(
                    request,
                    messages.INFO,
                    "Your Membership Duration is Increased!!",
                    extra_tags="custom",
                )
            context = {
                "form": UploadFileForm(),
                "date": str(User.membership_date),
                "USER": USER,
                "msgs": msgs,
                "swimming_slots": swimming_slots2,
                "swimming_slots_count": swimming_slots_count,
                "course_slots": course_slots2,
                "course_slots_count": course_slots_count,
                "game_slots": game_slots2,
                "game_slots_count": game_slots_count,
                "bookings_count": bookings_count,
                "upcoming_bookings": bookings2,
                "messages": messages.get_messages(request),
                "messages_object": messages_object2,
                "messages_object_count": messages_object_count,
            }
            return render(request, "userPortal/memberDateExtension.html", context)
        else:
            m = Membership_form.objects.filter(user=User)
            if len(m) > 0:
                if m[
                    0
                ].is_approved:  # If the User is still a non-member and the form isn't approved yet
                    m = m[0]
                    return render(request, "userPortal/nonMemberStatus.html", {})
                else:  # If the User's form is rejected..
                    if request.GET.get("resubmit") is "1":
                        try:
                            if request.session["resubmit"] == 0:
                                request.session["resubmit"] += 1
                                context = {
                                    "reason": m[0].reason,
                                    "USER": User,
                                    "msgs": msgs,
                                    "swimming_slots": swimming_slots2,
                                    "swimming_slots_count": swimming_slots_count,
                                    "course_slots": course_slots2,
                                    "course_slots_count": course_slots_count,
                                    "game_slots": game_slots2,
                                    "game_slots_count": game_slots_count,
                                    "bookings_count": bookings_count,
                                    "upcoming_bookings": bookings2,
                                    "messages": messages.get_messages(request),
                                    "messages_object": messages_object2,
                                    "messages_object_count": messages_object_count,
                                }
                                return render(
                                    request,
                                    "userPortal/nonMDisapproved.html",
                                    context=context,
                                )
                        except:
                            m = m[0]
                            m.delete()
                    else:
                        context = {
                            "reason": m[0].reason,
                            "messages": messages.get_messages(request),
                            "USER": User,
                            "msgs": msgs,
                            "swimming_slots": swimming_slots2,
                            "swimming_slots_count": swimming_slots_count,
                            "course_slots": course_slots2,
                            "course_slots_count": course_slots_count,
                            "game_slots": game_slots2,
                            "game_slots_count": game_slots_count,
                            "bookings_count": bookings_count,
                            "upcoming_bookings": bookings2,
                            "messages": messages.get_messages(request),
                            "messages_object": messages_object2,
                            "messages_object_count": messages_object_count,
                        }
                        return render(
                            request, "userPortal/nonMDisapproved.html", context=context
                        )
            # Form for applying for Membership
            form = UploadFileForm()
            if request.method == "POST":
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        User = NewUser.objects.filter(username=request.user.username)[0]
                    except:
                        User = Member.objects.filter(username=request.user.username)[0]
                    k = len(Membership_form.objects.all())
                    m = Membership_form.objects.filter(user=User)
                    if k == 0:
                        k = 1
                    else:
                        k = Membership_form.objects.all()[k - 1].id + 1
                    m = Membership_form(
                        id=k,
                        user=User,
                        ACardNum=request.POST.get("aCardNum"),
                        num_months=request.POST.get("num_months"),
                        phone_num=request.POST.get("phone_num"),
                        cert=request.FILES["file"],
                    )
                    m.save()
                    request.session["resubmit"] = 0
                    return render(request, "userPortal/nonMemberStatus.html", {})
            USER = NewUser.objects.get(username=request.user.username)
            context = {
                "form": form,
                "messages": messages.get_messages(request),
                "USER": USER,
                "msgs": msgs,
                "swimming_slots": swimming_slots2,
                "swimming_slots_count": swimming_slots_count,
                "course_slots": course_slots2,
                "course_slots_count": course_slots_count,
                "game_slots": game_slots2,
                "game_slots_count": game_slots_count,
                "bookings_count": bookings_count,
                "upcoming_bookings": bookings2,
                "messages": messages.get_messages(request),
                "messages_object": messages_object2,
                "messages_object_count": messages_object_count,
            }
            return render(request, "userPortal/registrationPage.html", context)
    else:
        return redirect("/login")


def confirmMembership(request):
    if (
        request.user is not None and request.user.username is not ""
    ):  # Authentication Checking
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        if (
            request.POST.get("reason") is not None
        ):  # If the Manager Disapproves a Form the Reason will be stored and updated
            id = int(request.POST.get("idx"))
            reason = request.POST.get("reason")
            form = Membership_form.objects.filter(id=id)
            if len(form) > 0:
                form = form[0]
                form.is_approved = False
                form.reason = reason
                form.save()
        elif (
            request.GET.get("approve") is "1"
        ):  # If the Manager Approves a Form, it updates user's details and deletes the form
            id = int(request.GET.get("id"))
            form = Membership_form.objects.filter(id=id)
            if len(form) > 0:
                form = form[0]
                User = form.user
                User.membership_date = datetime.today()
                User.membership_date += timedelta(days=int(form.num_months) * 30)
                User.membership_date = User.membership_date.date()
                User.aCardNum = form.ACardNum
                User.cert = form.cert
                User.phone_num = form.phone_num
                User.save()
                form.delete()
                messages.add_message(
                    request,
                    messages.INFO,
                    User.username + " is a Member now",
                    extra_tags="custom",
                )
        elif request.GET.get("remove") is "1":  # Manager removes the disapproved Form
            id = int(request.GET.get("id"))
            form = Membership_form.objects.filter(id=id, removed=False)
            if len(form) > 0:
                form = form[0]
                form.removed = True
                form.save()
        forms = Membership_form.objects.filter(is_approved=True)
        if len(forms) > 0:
            fb = 1
        else:
            fb = 0
        dforms = Membership_form.objects.filter(is_approved=False, removed=False)
        if len(dforms) > 0:
            dfb = 1
        else:
            dfb = 0
        context = {
            "USER": USER,
            "forms": forms,
            "dforms": dforms,
            "fb": fb,
            "dfb": dfb,
            "messages": messages.get_messages(request),
            "msgs": msgs,
            "swimming_slots": swimming_slots2,
            "swimming_slots_count": swimming_slots_count,
            "course_slots": course_slots2,
            "course_slots_count": course_slots_count,
            "game_slots": game_slots2,
            "game_slots_count": game_slots_count,
            "bookings_count": bookings_count,
            "upcoming_bookings": bookings2,
            "messages": messages.get_messages(request),
            "messages_object": messages_object2,
            "messages_object_count": messages_object_count,
        }
        return render(request, "userPortal/confirmMembership.html", context)
    else:
        return redirect("/login")


def course(request):
    if request.user is None or request.user.username is "":
        return redirect("/login/")

    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

    if request.GET.get("course_reg"):
        User = NewUser.objects.filter(username=request.user.username)[0]
        if User.type == "MANAGER":
            return managerCourseHome(request)
        courses = User.course.all()
        if len(courses) > 0:
            try:
                course = courses.get(name=request.GET.get("course_reg"))
            except:
                course = None
            if course is None:
                course = request.GET.get("course_reg")
                course = Course.objects.get(name=course)
                User.course.add(course)
                User.course_last_date = date.today() + timedelta(
                    days=int(30 * int(request.GET.get("duration")))
                )
                course.num_students += 1
                course.save()
                User.course_count += 1
                User.save()
                msgs = Message.objects.filter(
                    Description="The course that you've been enrolled is completed!! Please enroll again for continuation"
                )
                for x in msgs:
                    if User in x.users:
                        x.Date = User.course_last_date
                        x.save()
                        break
                msgs = Message.objects.filter(
                    Description="The course that you've been enrolled is completed!! Please enroll again for continuation"
                )
                for x in msgs:
                    if User in x.users:
                        x.Date = User.course_last_date
                        x.save()
                        break
                messages.add_message(
                    request,
                    messages.INFO,
                    "You are enrolled in the course " + course.name,
                    extra_tags="custom",
                )
        else:
            course = request.GET.get("course_reg")
            course = Course.objects.get(name=course)
            User.course.add(course)
            User.course_last_date = date.today() + timedelta(
                days=int(30 * int(request.GET.get("duration")))
            )
            User.save()
            course.num_students += 1
            course.save()
            messages.add_message(
                request,
                messages.INFO,
                "You are enrolled in the course " + course.name,
                extra_tags="custom",
            )
    USER = NewUser.objects.get(username=request.user.username)
    if USER.type == "MANAGER":
        return managerCourseHome(request)
    courses = USER.course.all()
    course_count = len(courses)
    context = {
        "USER": USER,
        "courses": courses,
        "course_count": course_count,
        "messages": messages.get_messages(request),
        "swimming_slots": swimming_slots2,
        "swimming_slots_count": swimming_slots_count,
        "course_slots": course_slots2,
        "course_slots_count": course_slots_count,
        "game_slots": game_slots2,
        "game_slots_count": game_slots_count,
        "bookings_count": bookings_count,
        "upcoming_bookings": bookings2,
        "messages": messages.get_messages(request),
        "messages_object": messages_object2,
        "messages_object_count": messages_object_count,
    }
    return render(request, "userPortal/course.html", context)


def coordinatorCoursePage(request):
    # shifting swimming and course slots by one week
    slots_ordering = Memberslot.objects.all()
    slots_course = Courseslot.objects.all()
    slots_ordering = list(slots_ordering) + list(slots_course)
    curr_date = datetime.now().date()
    Day = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
    mon_date = curr_date - timedelta(days=Day + 1)
    for Slots in slots_ordering:
        while Slots.Date < mon_date:
            Slots.Date = Slots.Date + timedelta(days=7)
            Slots.save()

    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        USER = NewUser.objects.get(username=request.user.username)
        courses = USER.course.all()
        context = {
            "courses": courses,
            "USER": USER,
            "msgs": msgs,
            "swimming_slots": swimming_slots2,
            "swimming_slots_count": swimming_slots_count,
            "course_slots": course_slots2,
            "course_slots_count": course_slots_count,
            "game_slots": game_slots2,
            "game_slots_count": game_slots_count,
            "bookings_count": bookings_count,
            "upcoming_bookings": bookings2,
            "messages": messages.get_messages(request),
            "messages_object": messages_object2,
            "messages_object_count": messages_object_count,
        }
        return render(request, "userPortal/coordinatorCoursePage.html", context)
    else:
        return redirect("/login")


def courseSlotRegister(request):
    if request.user is not None and request.user.username is not "":
        USER = NewUser.objects.get(username=request.user.username)
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        if request.GET.get("add") is "0":
            SLOT = Courseslot.objects.get(id=request.GET.get("id"))
            SLOT.rem_num_participants = 50
            course = Course.objects.get(id=request.GET.get("idx"))
            SLOT.course.remove(course)
            SLOT.save()
            messages.add_message(
                request, messages.INFO, "Slot removed!!", extra_tags="custom"
            )
            return redirect(
                "/userPortal/courseSlotRegister/?idx=" + request.GET.get("idx")
            )
        elif request.GET.get("add") is "1":
            Course2 = Course.objects.get(id=request.GET.get("idx"))
            if Course2.slot_set.all().count() is 3:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Limit of 3 Coures slots reached!!",
                    extra_tags="custom",
                )
                return redirect(
                    "/userPortal/courseSlotRegister/?idx=" + request.GET.get("idx")
                )
            else:
                SLOT = Courseslot.objects.get(id=request.GET.get("id"))
                SLOT.course.add(Course2)
                SLOT.rem_num_participants = 0
                SLOT.save()
                messages.add_message(
                    request, messages.INFO, "Slot Added!!", extra_tags="custom"
                )
                return redirect(
                    "/userPortal/courseSlotRegister/?idx=" + request.GET.get("idx")
                )
        available_slots = (
            Courseslot.objects.filter(type="COURSESLOT")
            .exclude(rem_num_participants="0")
            .order_by("Date")
        )
        for comp_booked in Competition.objects.all():
            available_slots = available_slots.exclude(Date=comp_booked.slot.Date)
        course3 = Course.objects.filter(id=request.GET.get("idx"))[0]
        slots3 = course3.slot_set.filter(type="COURSESLOT").order_by("Date")
        slots_count = slots3.count()
        lst = []
        for x in course_slots2:
            lst.append((x, x.course.all()[0].name))
        context = {
            "course": course3,
            "slots_count": slots_count,
            "available_slots": available_slots,
            "USER": USER,
            "msgs": msgs,
            "swimming_slots": swimming_slots2,
            "swimming_slots_count": swimming_slots_count,
            "course_slots": tuple(lst),
            "course_slots_count": course_slots_count,
            "game_slots": game_slots2,
            "game_slots_count": game_slots_count,
            "bookings_count": bookings_count,
            "upcoming_bookings": bookings2,
            "messages": messages.get_messages(request),
            "messages_object": messages_object2,
            "messages_object_count": messages_object_count,
        }
        return render(request, "userPortal/courseSlotRegister.html", context)
    else:
        return redirect("/login")


def managerCourseHome(request):
    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        courses = Course.objects.all()  # Passing the List of All Courses
        context = {
            "courses": courses,
            "messages": messages.get_messages(request),
            "USER": USER,
            "msgs": msgs,
            "swimming_slots": swimming_slots2,
            "swimming_slots_count": swimming_slots_count,
            "course_slots": course_slots2,
            "course_slots_count": course_slots_count,
            "game_slots": game_slots2,
            "game_slots_count": game_slots_count,
            "bookings_count": bookings_count,
            "upcoming_bookings": bookings2,
            "messages": messages.get_messages(request),
            "messages_object": messages_object2,
            "messages_object_count": messages_object_count,
        }
        return render(request, "userPortal/managerCourseHome.html", context)
    else:
        return redirect("/login")


def managerCreateCourse(request):
    if request.user is not None and request.user.username is not "":
        USER = NewUser.objects.get(username=request.user.username)
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        if request.method == "POST":
            courses = Course.objects.all()
            k = 0
            for x in courses:
                k = x.id
            k += 1
            crs = Course(
                id=k,
                name=request.POST.get("name"),
                start_date=request.POST.get("date"),
                cost=request.POST.get("cost"),
            )  # Create a Course based on Given info
            crs.save()
            coordinator = Coordinator.objects.get(username=request.POST.get("cName"))
            coordinator.course.add(crs)
            coordinator.save()
            messages.add_message(
                request,
                messages.INFO,
                "Course " + crs.name + " Created",
                extra_tags="custom",
            )
            return redirect("/userPortal/course/")
        coors = Coordinator.objects.all()
        if len(coors) > 0:
            cr = coors[0].username
        else:
            cr = None
        context = {
            "coors": coors,
            "coorName": cr,
            "USER": USER,
            "msgs": msgs,
            "swimming_slots": swimming_slots2,
            "swimming_slots_count": swimming_slots_count,
            "course_slots": course_slots2,
            "course_slots_count": course_slots_count,
            "game_slots": game_slots2,
            "game_slots_count": game_slots_count,
            "bookings_count": bookings_count,
            "upcoming_bookings": bookings2,
            "messages": messages.get_messages(request),
            "messages_object": messages_object2,
            "messages_object_count": messages_object_count,
        }
        return render(request, "userPortal/managerCreateCourse.html", context)
    else:
        return redirect("/login")


def comp(request):
    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        if USER.type == "MANAGER":
            return ManagerCompHome(request)
        comp = Competition.objects.all()
        lst = []
        plst = []  # Passing Competition and corresponding Games info to Display them
        for x in comp:
            cslot = Compslot.objects.get(competition=x)
            pst = []
            for y in x.game_set.all():
                gslot = Gameslot.objects.filter(game=y)[0]
                kst = []
                if USER in gslot.users.all():
                    kst.append(y)
                    kst.append(gslot)
                    kst.append(50 - gslot.rem_num_participants)
                    pst.append(tuple(kst))
            if cslot.Date >= date.today() and len(pst) > 0:
                lst.append((x, cslot, len(pst), tuple(pst)))
            elif len(pst) > 0:
                plst.append((x, cslot, len(pst), tuple(pst)))
        context = {
            "USER": USER,
            "msgs": msgs,
            "swimming_slots": swimming_slots2,
            "swimming_slots_count": swimming_slots_count,
            "course_slots": course_slots2,
            "course_slots_count": course_slots_count,
            "game_slots": game_slots2,
            "game_slots_count": game_slots_count,
            "bookings_count": bookings_count,
            "upcoming_bookings": bookings2,
            "data": lst,
            "num": len(lst),
            "pnum": len(plst),
            "pdata": plst,
            "messages": messages.get_messages(request),
            "messages_object": messages_object2,
            "messages_object_count": messages_object_count,
        }
        return render(request, "userPortal/comp.html", context)
    else:
        return redirect("/login")


def ManagerCompHome(request):
    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

    comp = (
        Competition.objects.all()
    )  # Passing the Data of All competitions and corresponding games to display
    lst = []
    plst = []
    for x in comp:
        cslot = Compslot.objects.get(competition=x)
        pst = []
        for y in x.game_set.all():
            gslot = Gameslot.objects.filter(game=y)[0]
            kst = [y, gslot, 50 - gslot.rem_num_participants]
            pst.append(tuple(kst))
        if cslot.Date >= date.today():
            lst.append((x, cslot, len(pst), tuple(pst)))
        else:
            plst.append((x, cslot, len(pst), tuple(pst)))
    game = Game.objects.all()
    gst = []
    for x in game:
        gslot = Gameslot.objects.filter(game=x)
        if len(gslot) > 0:
            gslot = gslot[0]
            gst.append((x, gslot, 50 - gslot.rem_num_participants))
        else:
            gslot = None
            gst.append((x, None, None))
    USER = NewUser.objects.get(username=request.user.username)
    context = {
        "data": lst,
        "num": len(lst),
        "pnum": len(plst),
        "pdata": plst,
        "gst": gst,
        "gnum": len(gst),
        "messages": messages.get_messages(request),
        "USER": USER,
        "msgs": msgs,
        "swimming_slots": swimming_slots2,
        "swimming_slots_count": swimming_slots_count,
        "course_slots": course_slots2,
        "course_slots_count": course_slots_count,
        "game_slots": game_slots2,
        "game_slots_count": game_slots_count,
        "bookings_count": bookings_count,
        "upcoming_bookings": bookings2,
        "messages": messages.get_messages(request),
        "messages_object": messages_object2,
        "messages_object_count": messages_object_count,
    }
    return render(request, "userPortal/managerCompHome.html", context)


def managerCreateComp(request):
    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        if request.method == "POST":  # Filter for data selected for previous days
            x = request.POST.get("slot")
            dat = datetime.date(datetime.strptime(x, "%Y-%m-%d"))
            if dat <= date.today():
                messages.add_message(
                    request,
                    messages.INFO,
                    "You can only create a competition for the upcoming days..",
                    extra_tags="custom",
                )
                return redirect("/userPortal/comp/")
            for x in Slot.objects.filter(
                Date=dat
            ):  # Filter to check Events on selected Date
                event_ = x.event
                try:
                    if event_.is_paid is True:
                        messages.add_message(
                            request,
                            messages.INFO,
                            "An Event has been booked on that date!! Please "
                            "select another date...",
                            extra_tags="custom",
                        )
                        return redirect("/userPortal/comp/")
                except:
                    pass
                if (
                    x.competition is not None
                ):  # Filter for Checking if a comp already Exists on the selected Date
                    messages.add_message(
                        request,
                        messages.INFO,
                        "A Competition already exists on that date!! Please "
                        "select another date...",
                        extra_tags="custom",
                    )
                    return redirect("/userPortal/comp/")

            m = Message(
                head="Swimming Slot Cancelled",
                Description="A Competition is held on "
                + str(dat)
                + ", so all the Slots including your Swimming Slot has been cancelled on "
                + str(dat)
                + ".",
                Date=dat,
            )
            m.save()  # Messages for Users about their slots cancellation
            for x in Memberslot.objects.filter(Date=dat):
                for y in x.users.all():
                    m.users.add(y)
                x.users.clear()
                x.rem_num_participants = 50
                x.save()
            m.save()
            m2 = Message(
                head="Course Slot Cancelled",
                Description="A Competition is held on "
                + str(dat)
                + ", so all the Slots including your Course Slot has been cancelled on "
                + str(dat)
                + ".",
                Date=dat,
            )
            m2.save()
            for courseSlot in Courseslot.objects.filter(Date=dat):
                for members in courseSlot.users.all():
                    m2.users.add(members)
                courseSlot.course.clear()
                courseSlot.rem_num_participants = 50
                courseSlot.save()
            m2.save()
            y = Compslot(from_time="7:00:00", to_time="10:00:00", Date=dat)
            y.Day = y.setDay(y.Date)
            y.save()  # Saving the respective Competition slot
            k = 1
            for p in Competition.objects.all():
                k = p.id + 1
            cp = Competition(id=k, name=request.POST.get("name"))
            cp.save()
            y.competition = cp
            y.save()
            for z in range(7, 10):  # Creating Gameslots for that date
                gs = Gameslot(
                    from_time=str(z) + ":00:00",
                    to_time=str(z) + ":30:00",
                    Date=y.Date,
                    Day=y.Day,
                )
                gs.save()
                gst = Gameslot(
                    from_time=str(z) + ":30:00",
                    to_time=str(z + 1) + ":00:00",
                    Date=y.Date,
                    Day=y.Day,
                )
                gst.save()
            messages.add_message(
                request,
                messages.INFO,
                "Competition " + cp.name + " Created",
                extra_tags="custom",
            )
            return redirect("/userPortal/comp/")
        USER = NewUser.objects.get(username=request.user.username)
        context = {
            "USER": USER,
            "msgs": msgs,
            "swimming_slots": swimming_slots2,
            "swimming_slots_count": swimming_slots_count,
            "course_slots": course_slots2,
            "course_slots_count": course_slots_count,
            "game_slots": game_slots2,
            "game_slots_count": game_slots_count,
            "bookings_count": bookings_count,
            "upcoming_bookings": bookings2,
            "messages": messages.get_messages(request),
            "messages_object": messages_object2,
            "messages_object_count": messages_object_count,
        }
        return render(request, "userPortal/managerCreateComp.html", context)
    else:
        return redirect("/login")


def managerCreateGame(request):
    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        if request.method == "POST":
            x = request.POST.get("slot")
            if "a" in x:
                x = x.split(" ")[0] + "AM"
            else:
                x = x.split(" ")[0] + "PM"
            try:
                y = datetime.strptime(x, "%I:%M%p")
            except:
                y = datetime.strptime(x, "%I%p")
            comp = Competition.objects.get(
                id=request.POST.get("comp_id")
            )  # Gets data from the form and get's the respective competition
            game = Game(
                from_age=request.POST.get("from_age"),
                to_age=request.POST.get("to_age"),
                gender=request.POST.get("cName"),
                game_type=request.POST.get("name"),
                competition=comp,
            )
            game.save()
            gslot = Gameslot.objects.filter(
                Date=Compslot.objects.get(competition=comp).Date,
                from_time=datetime.time(y),
            )[0]
            gslot.game = game
            gslot.save()
            messages.add_message(
                request,
                messages.INFO,
                "Game " + game.game_type + " Added to Competition " + comp.name,
                extra_tags="custom",
            )
            return redirect(
                "/userPortal/comp/#collapseExample" + request.POST.get("comp_id")
            )
        if request.GET.get("comp_id") is not None and request.POST.get("name") is None:
            comp = Competition.objects.get(id=request.GET.get("comp_id"))
            cslot = Compslot.objects.get(competition=comp)
            lst = []
            for (
                x
            ) in (
                Gameslot.objects.all()
            ):  # Filters the Data if there is no game in those gameslots
                if x.Date == cslot.Date and x.game is None:
                    lst.append(x)
            context = {
                "comp": comp,
                "gslots": lst,
                "USER": USER,
                "msgs": msgs,
                "swimming_slots": swimming_slots2,
                "swimming_slots_count": swimming_slots_count,
                "course_slots": course_slots2,
                "course_slots_count": course_slots_count,
                "game_slots": game_slots2,
                "game_slots_count": game_slots_count,
                "bookings_count": bookings_count,
                "upcoming_bookings": bookings2,
                "messages": messages.get_messages(request),
                "messages_object": messages_object2,
                "messages_object_count": messages_object_count,
            }
        else:
            context = {
                "USER": USER,
                "msgs": msgs,
                "swimming_slots": swimming_slots2,
                "swimming_slots_count": swimming_slots_count,
                "course_slots": course_slots2,
                "course_slots_count": course_slots_count,
                "game_slots": game_slots2,
                "game_slots_count": game_slots_count,
                "bookings_count": bookings_count,
                "upcoming_bookings": bookings2,
                "messages": messages.get_messages(request),
                "messages_object": messages_object2,
                "messages_object_count": messages_object_count,
            }
        return render(request, "userPortal/managerCreateGame.html", context)
    else:
        return redirect("/login")


def event(request):
    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

    slots_ordering = Memberslot.objects.all()
    slots_course = Courseslot.objects.all()
    slots_ordering = list(slots_ordering) + list(slots_course)
    curr_date = datetime.now().date()
    Day = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
    mon_date = curr_date - timedelta(days=Day + 1)
    ucount = 0
    pcount = 0
    upcoming_list = []
    past_list = []
    for Slots in slots_ordering:
        while Slots.Date < mon_date:
            Slots.Date = Slots.Date + timedelta(days=7)
            Slots.save()
    if request.user is not None and request.user.username is not "":
        if request.GET.get("cancel") is "1":
            event_date = request.GET.get("date")
            event_date = date.strftime(
                datetime.strptime(event_date, "%B %d, %Y"), "%Y-%m-%d"
            )
            event_ = EventBooking.objects.filter(Date=event_date)[0]
            event_.delete()
            events = Event.objects.filter(userid=request.user.username)
            slot = Eventslot.objects.get(Date=event_date)
            e = slot.event
            e.userid = None
            e.is_paid = False
            e.isBooked = False
            e.save()
        USER = NewUser.objects.filter(username=request.user.username)[0]
        if USER.type == "MANAGER":
            lst = EventBooking.objects.all()
            count = EventBooking.objects.all().count()
        else:
            lst = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
            count = EventBooking.objects.filter(user_aadhar=USER.aCardNum).count()
        curr_date = date.today()
        curr_time = datetime.now().time()
        if count > 0:
            for booking in lst:
                y = Eventslot.objects.get(Date=booking.Date)
                if y.event.is_paid is False:
                    booking.delete()
                    continue
                if booking.Date < curr_date:
                    past_list.append(booking)
                    pcount += 1
                else:
                    if (
                        booking.Date == curr_date
                        and booking.to_time.hour > curr_time.hour
                    ):
                        upcoming_list.append(booking)
                        ucount += 1
                    elif (
                        booking.Date == curr_date
                        and booking.to_time.hour <= curr_time.hour
                    ):
                        past_list.append(booking)
                        pcount += 1
                    else:
                        upcoming_list.append(booking)
                        ucount += 1
        context = {
            "past_bookings": past_list,
            "upcoming_bookings": upcoming_list,
            "pcount": pcount,
            "ucount": ucount,
            "USER": USER,
            "msgs": msgs,
            "swimming_slots": swimming_slots2,
            "swimming_slots_count": swimming_slots_count,
            "course_slots": course_slots2,
            "course_slots_count": course_slots_count,
            "game_slots": game_slots2,
            "game_slots_count": game_slots_count,
            "bookings_count": bookings_count,
            "messages": messages.get_messages(request),
            "messages_object": messages_object2,
            "messages_object_count": messages_object_count,
        }
        return render(request, "userPortal/event.html", context)
    else:
        return redirect("/login")


def suggestion(request):
    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

        if USER.type != "MEMBER":  # Checking for Manager Privileges
            return otherSuggestion(request)
        lst = []
        pst = []
        dpst = []
        for y in Feedback.objects.all():  # Filtering the Feedback Objects
            if USER in y.user.all():
                dpst.append(y)
        for x in dpst:
            if x.replied:
                if len(x.persons.all()) > 1:
                    pst.append((x, "None"))
                else:
                    pst.append((x, x.persons.all()[0].username))
            else:
                if len(x.persons.all()) > 1:
                    lst.append((x, "None"))
                else:
                    lst.append((x, x.persons.all()[0].username))
        context = {
            "forms": lst,
            "fb": len(lst),
            "pforms": pst,
            "pb": len(pst),
            "USER": USER,
            "msgs": msgs,
            "swimming_slots": swimming_slots2,
            "swimming_slots_count": swimming_slots_count,
            "course_slots": course_slots2,
            "course_slots_count": course_slots_count,
            "game_slots": game_slots2,
            "game_slots_count": game_slots_count,
            "bookings_count": bookings_count,
            "upcoming_bookings": bookings2,
            "messages": messages.get_messages(request),
            "messages_object": messages_object2,
            "messages_object_count": messages_object_count,
        }
        return render(request, "userPortal/suggestion.html", context)
    else:
        return redirect("/login")


def otherSuggestion(request):
    if request.user is not None and request.user.username is not "":
        # notifications
        USER = NewUser.objects.get(username=request.user.username)
        # swimming slots
        swimming_slots = USER.slot_set.filter(type="MEMBERSLOT").order_by("Date")
        swimming_slots2 = list(swimming_slots)
        curr_date = datetime.now().date()
        TDay = datetime.strptime(str(curr_date), "%Y-%m-%d").weekday()
        for s in swimming_slots:
            SDay = datetime.strptime(str(s.Date), "%Y-%m-%d").weekday()
            if SDay < TDay:
                swimming_slots2.remove(s)
        swimming_slots_count = len(swimming_slots2)
        msgs = Message.objects.all()

        # courses
        course_slots2 = []
        courses = USER.course.all()
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay:
                    course_slots2.append(course_slot)
        for course in courses:
            course_slots = course.slot_set.all()
            for course_slot in course_slots:
                SDay = datetime.strptime(str(course_slot.Date), "%Y-%m-%d").weekday()
                if SDay == TDay + 1:
                    course_slots2.append(course_slot)
        course_slots_count = len(course_slots2)

        # competitions
        game_slots2 = []
        game_slots = USER.slot_set.filter(type="GAMESLOT")
        for game_slot in game_slots:
            if game_slot.Date > curr_date:
                delta = game_slot.Date - curr_date
                if delta.days < 7:
                    game_slots2.append(game_slot)
        game_slots_count = len(game_slots2)

        # events
        bookings2 = []
        bookings = EventBooking.objects.filter(user_aadhar=USER.aCardNum)
        for booking in bookings:
            if booking.Date > curr_date:
                delta = booking.Date - curr_date
                if delta.days < 7:
                    bookings2.append(booking)
        bookings_count = len(bookings2)

        # messages
        messages_object2 = []
        messages_object = USER.message_set.all()
        for message_object in messages_object:
            if message_object.Date > curr_date:
                delta = message_object.Date - curr_date
                if delta.days < 3:
                    messages_object2.append(message_object)
        messages_object_count = len(messages_object2)

    if request.method == "POST":  # Saves the Feedback object with the provided reply
        form = Feedback.objects.get(id=request.POST.get("idx"))
        form.reply = request.POST.get("reply")
        form.replied = True
        form.save()
    lst = []
    pst = []
    dpst = []
    USER = NewUser.objects.get(username=request.user.username)
    if USER.type == "MANAGER":
        dpst = Feedback.objects.all()
    else:
        for y in Feedback.objects.all():
            if USER in y.persons.all():
                dpst.append(y)
    for x in dpst:  # Filters the Feedback objects
        if x.replied:
            if len(x.persons.all()) > 1:
                pst.append((x, x.user.all()[0], "None"))
            else:
                pst.append((x, x.user.all()[0], x.persons.all()[0].username))
        else:
            if len(x.persons.all()) > 1:
                lst.append((x, x.user.all()[0], "None"))
            else:
                lst.append((x, x.user.all()[0], x.persons.all()[0].username))
    context = {
        "forms": lst,
        "fb": len(lst),
        "pforms": pst,
        "pb": len(pst),
        "USER": USER,
        "msgs": msgs,
        "swimming_slots": swimming_slots2,
        "swimming_slots_count": swimming_slots_count,
        "course_slots": course_slots2,
        "course_slots_count": course_slots_count,
        "game_slots": game_slots2,
        "game_slots_count": game_slots_count,
        "bookings_count": bookings_count,
        "upcoming_bookings": bookings2,
        "messages": messages.get_messages(request),
        "messages_object": messages_object2,
        "messages_object_count": messages_object_count,
    }
    return render(request, "userPortal/otherSuggestion.html", context)
