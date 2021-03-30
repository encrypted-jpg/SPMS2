from django.shortcuts import render, redirect
from django.urls import reverse
from . import templates
from apps.suggestionPortal.models import Feedback
from mysite.models import Member, NewUser, Coordinator, Committee, Manager
from apps.coursePage.models import Course

# Create your views here.


def index(request):
    if request.user is not None and request.user.username is not "":
        if request.GET.get("name") is not None:
            name = request.GET.get("name")
            area = request.GET.get("area")
            message = request.GET.get("message")
            person = request.GET.get("service")
            f = Feedback(id=len(Feedback.objects.all()) + 1, name=name, text=message)
            f.save()
            if person == "Select Person":
                f.is_manager = True
            else:
                person = Coordinator.objects.filter(username=person)[0]
                f.coordinators.add(person)

            try:
                m = Member.objects.filter(username=request.user.username)[0]
                f.member.add(m)
            except:
                m = NewUser.objects.filter(username=request.user.username)[0]
                f.nonmember.add(m)
            f.save()
            return redirect("/userPortal")
        if request.GET.get("area"):
            coorName = Coordinator.objects.filter(
                course=Course.objects.filter(name=request.GET.get("area"))[0]
            )[0].username
            context = {
                "users": list(Coordinator.objects.all())
                + list(Committee.objects.all())
                + list(Manager.objects.all()),
                "area": request.GET.get("area"),
                "coorName": coorName,
            }
        else:
            context = {
                "users": list(Coordinator.objects.all())
                + list(Committee.objects.all())
                + list(Manager.objects.all()),
                "area": "",
                "coorName": "Select person",
            }
        return render(request, "suggestionPortal/index.html", context)
    request.session["next"] = "/suggestionPortal"
    return redirect("/login")
