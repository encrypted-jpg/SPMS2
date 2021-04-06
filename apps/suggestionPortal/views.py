from django.shortcuts import render, redirect
from django.urls import reverse
from . import templates
from apps.suggestionPortal.models import Feedback
from mysite.models import Member, NewUser, Coordinator, Committee, Manager
from apps.coursePage.models import Course
from django.contrib import messages
from datetime import date


# Create your views here.


def index(request):
    if (
        request.user is not None and request.user.username is not ""
    ):  # Checks for Authentication
        if request.GET.get("name") is not None:
            USER = NewUser.objects.get(username=request.user.username)
            if USER.type == "MANAGER":  # Check if the User is a Manager
                messages.add_message(
                    request,
                    messages.INFO,
                    "You are a Manager!! This Functionality is Working " "Properly..",
                    extra_tags="custom",
                )
                return redirect("/userPortal")
            name = request.GET.get("name")
            area = request.GET.get("area")
            message = request.GET.get("message")
            person = request.GET.get("service")
            person = NewUser.objects.get(first_name=person.split()[0]).username
            f = Feedback(
                id=len(Feedback.objects.all()) + 1,
                name=name,
                text=message,
                date=date.today(),
            )
            f.save()  # Retrieves the data and saves the Feedback object
            if person == "Select person":
                for comm_ in Committee.objects.all():
                    f.persons.add(comm_)
            else:
                person = NewUser.objects.filter(username=person)[0]
                f.persons.add(person)
            m = NewUser.objects.filter(username=request.user.username)[0]
            f.user.add(m)
            f.save()
            messages.add_message(
                request,
                messages.INFO,
                "Your Response will be notified to the respective person.",
                extra_tags="custom",
            )  # Displays a Message of Success in userportal
            return redirect("/userPortal/suggestion")
        if request.GET.get(
            "area"
        ):  # If this page is being redirected from a Course Complain Page, it adds few values
            coor = Coordinator.objects.filter(
                course=Course.objects.filter(name=request.GET.get("area"))[0]
            )[0]
            coorName = coor.first_name
            coorName2 = coor.last_name
            context = {
                "users": list(Coordinator.objects.all())
                + list(Committee.objects.all())
                + list(Manager.objects.all()),
                "area": request.GET.get("area"),
                "coorName": coorName,
                "coorName2": coorName2,
            }
        else:
            context = {
                "users": list(Coordinator.objects.all())
                + list(Committee.objects.all())
                + list(Manager.objects.all()),
                "area": "",
                "coorName": "Select person",
                "coorName2": "",
            }  # Displays the suggestion Page
        return render(request, "suggestionPortal/index.html", context)
    request.session["next"] = request.get_full_path()
    return redirect("/login")
