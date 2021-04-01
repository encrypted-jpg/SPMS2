from django.shortcuts import render, redirect
from django.urls import reverse
from . import templates
from mysite.models import *
from apps.coursePage.models import Course
from .forms import UploadFileForm
from .models import Membership_form
from datetime import datetime, timedelta, date
import os


# Create your views here.


def index(request):
    if request.user is None or request.user.username is "":
        return redirect("/login/")
    if request.GET.get("course_reg"):
        try:
            User = Member.objects.filter(username=request.user.username)[0]
        except:
            User = NewUser.objects.filter(username=request.user.username)[0]
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
                User.save()
        else:
            course = request.GET.get("course_reg")
            course = Course.objects.get(name=course)
            User.course.add(course)
            User.save()
    available_slots = Slot.objects.all()
    USER = NewUser.objects.get(username=request.user.username)
    msgs = Message.objects.all()
    context = {"available_slots": available_slots, "USER": USER, "msgs": msgs}
    return render(request, "userPortal/index.html", context)


def slots(request):
    USER = NewUser.objects.get(username=request.user.username)
    context = {}
    return render(request, "userPortal/slots.html", context)


def availableSlots(request):
    if request.user is not None and request.user.username is not "":
        USER = NewUser.objects.get(username=request.user.username)
        if request.GET.get("add") is "0":
            SLOT = Memberslot.objects.get(id=request.GET.get("id"))
            SLOT.rem_num_participants = SLOT.rem_num_participants+1
            SLOT.users.remove(USER)
            print(request.GET.get("add"), request.GET.get("id"), SLOT)
        elif request.GET.get("add") is "1":
            print("YO", USER.slot_set.filter(type="MEMBERSLOT"))
            SLOT = Memberslot.objects.get(id=request.GET.get("id"))
            SLOT.rem_num_participants = SLOT.rem_num_participants-1
            SLOT.users.add(USER)
            SLOT.save()
            print(USER.slot_set.filter(type="MEMBERSLOT"))
            print(request.GET.get("add"), request.GET.get("id"), SLOT)
        monday_slots = Memberslot.objects.filter(Day="Monday").exclude(rem_num_participants="0")
        tuesday_slots = Memberslot.objects.filter(Day="Tuesday").exclude(rem_num_participants="0")
        wednesday_slots = Memberslot.objects.filter(Day="Wednesday").exclude(rem_num_participants="0")
        thursday_slots = Memberslot.objects.filter(Day="Thursday").exclude(rem_num_participants="0")
        saturday_slots = Memberslot.objects.filter(Day="Saturday").exclude(rem_num_participants="0")
        friday_slots = Memberslot.objects.filter(Day="Friday").exclude(rem_num_participants="0")
        sunday_slots = Memberslot.objects.filter(Day="Sunday").exclude(rem_num_participants="0")
        slots = USER.slot_set.filter(type="MEMBERSLOT")
        for idx in slots:
            monday_slots = monday_slots.exclude(id=idx.id)
            tuesday_slots = tuesday_slots.exclude(id=idx.id)
            wednesday_slots = wednesday_slots.exclude(id=idx.id)
            thursday_slots = thursday_slots.exclude(id=idx.id)
            friday_slots = friday_slots.exclude(id=idx.id)
            saturday_slots = saturday_slots.exclude(id=idx.id)
            sunday_slots = sunday_slots.exclude(id=idx.id)
        context = {
            "slots": slots,
            "monday_slots": monday_slots,
            "tuesday_slots": tuesday_slots,
            "wednesday_slots": wednesday_slots,
            "thursday_slots": thursday_slots,
            "friday_slots": friday_slots,
            "saturday_slots": saturday_slots,
            "sunday_slots": sunday_slots,
            "USER": USER,
        }
        return render(request, "userPortal/availableSlots.html", context)
    else:
        return redirect("/login")


def handle_uploaded_file(f, name):
    path = os.path.join(os.path.abspath(os.getcwd()), "apps\\userPortal\\data\\" + name)
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def registrationPage(request):
    if request.user is not None and request.user.username is not "":
        User = NewUser.objects.get(username=request.user.username)
        if not str(User.membership_date) == "2001-01-01":
            m = Membership_form.objects.filter(user=User)
            # Is a Member display expiration data/ option for extension
            if request.POST.get("num_months") is not None:
                num = request.POST.get("num_months")
                User.membership_date = datetime.strptime(
                    str(User.membership_date), "%Y-%m-%d"
                )
                User.membership_date += timedelta(days=int(num) * 30)
                User.membership_date = User.membership_date.date()
                User.save()
            context = {"form": UploadFileForm(), "date": str(User.membership_date)}
            return render(request, "userPortal/memberDateExtension.html", context)
        else:
            m = Membership_form.objects.filter(user=User)
            if len(m) > 0:
                if m[0].is_approved:
                    # is not a member display approval status
                    m = m[0]
                    return render(request, "userPortal/nonMemberStatus.html", {})
                else:
                    if request.GET.get("resubmit") is "1":
                        try:
                            if request.session["resubmit"] == 0:
                                request.session["resubmit"] += 1
                                context = {"reason": m[0].reason}
                                return render(
                                    request,
                                    "userPortal/nonMDisapproved.html",
                                    context=context,
                                )
                        except:
                            m = m[0]
                            m.delete()
                    else:
                        context = {"reason": m[0].reason}
                        return render(
                            request, "userPortal/nonMDisapproved.html", context=context
                        )
            # is not a member display form
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
                    # handle_uploaded_file(request.FILES["file"], request.user.username + "_Mship_file.pdf")
            USER = NewUser.objects.get(username=request.user.username)
            context = {
                "form": form,
                "USER": USER,
            }
            return render(request, "userPortal/registrationPage.html", context)
    else:
        return redirect("/login")


def confirmMembership(request):
    if request.user is not None and request.user.username is not "":
        if request.POST.get("reason") is not None:
            id = int(request.POST.get("idx"))
            reason = request.POST.get("reason")
            form = Membership_form.objects.filter(id=id)
            if len(form) > 0:
                form = form[0]
                form.is_approved = False
                form.reason = reason
                form.save()
        elif request.GET.get("approve") is "1":
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
        elif request.GET.get("remove") is "1":
            id = int(request.GET.get("id"))
            form = Membership_form.objects.filter(id=id, removed=False)
            if len(form) > 0:
                form = form[0]
                form.removed = True
                form.save()
        USER = NewUser.objects.get(username=request.user.username)
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
        }
        return render(request, "userPortal/confirmMembership.html", context)
    else:
        return redirect("/login")


def course(request):
    if request.user is not None and request.user.username is not "":
        USER = NewUser.objects.get(username=request.user.username)
        courses = USER.course.all()
        context = {
            "USER": USER,
            "courses": courses,
        }
        return render(request, "userPortal/course.html", context)
    else:
        return redirect("/login")


def comp(request):
    USER = NewUser.objects.get(username=request.user.username)
    comp = Competition.objects.all()
    lst = []
    plst = []
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
        if cslot.Date >= date.today():
            lst.append((x, cslot, len(pst), tuple(pst)))
        else:
            plst.append((x, cslot, len(pst), tuple(pst)))
    print(lst)
    context = {
        "USER": USER,
        "data": lst,
        "num": len(lst),
        "pnum": len(plst),
        "pdata": plst,
    }
    return render(request, "userPortal/comp.html", context)


def event(request):
    USER = NewUser.objects.get(username=request.user.username)
    context = {
        "USER": USER,
    }
    return render(request, "userPortal/event.html", context)
