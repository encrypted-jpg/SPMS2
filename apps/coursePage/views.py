from django.contrib import messages
from django.shortcuts import render, redirect

from mysite.models import *


# Create your views here.


def index(request):  # Renders Courses Home Page
    courses = Course.objects.all()
    context = {"courses": courses}
    return render(request, "coursePage/index.html", context=context)


def registration(request):  # Displays the Payment Page
    if request.user is not None and request.user.username is not "":
        User = NewUser.objects.get(username=request.user.username)
        if User.type == "MANAGER":  # Checks if the User is a Manager
            messages.add_message(
                request,
                messages.INFO,
                "You are a Manager!! This Functionality is Working Properly..",
                extra_tags="custom",
            )
            return redirect("/userPortal/course")
        courses = User.course.all()
        if len(courses) > 0:  # Checks if the User is already enrolled in a Course
            try:
                course = courses.get(name=request.GET.get("course"))
            except:
                course = None
            if course is None:
                cost = (
                    int(request.GET.get("duration"))
                    * Course.objects.get(name=request.GET.get("course")).cost
                )
                return render(
                    request,
                    "coursePage/register.html",
                    {
                        "course": request.GET.get("course"),
                        "duration": request.GET.get("duration"),
                        "cost": cost,
                    },
                )
            else:
                messages.add_message(
                    request,
                    messages.INFO,
                    "You are already enrolled in this course!!",
                    extra_tags="custom",
                )
                return redirect("/userPortal/course")
        else:  # if the user is not enrolled in any course then the user is will be redirected to Payment Page
            cost = (
                int(request.GET.get("duration"))
                * Course.objects.get(name=request.GET.get("course")).cost
            )
            return render(
                request,
                "coursePage/register.html",
                {
                    "course": request.GET.get("course"),
                    "duration": request.GET.get("duration"),
                    "cost": cost,
                },
            )
    request.session["next"] = (
        "/coursePage/register?course="
        + request.GET.get("course")
        + "&duration="
        + request.GET.get("duration")
    )
    return redirect("/login")
