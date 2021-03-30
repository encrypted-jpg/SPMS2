from django.shortcuts import render, redirect
from django.urls import reverse
from . import templates
from django.contrib import messages
from .models import Course
from mysite.models import *


# Create your views here.


def index(request):
    courses = Course.objects.all()
    context = {"courses": courses}
    return render(request, "coursePage/index.html", context=context)


def registration(request):
    if request.user is not None and request.user.username is not "":
        print(request.GET.get("duration"))
        try:
            User = Member.objects.get(username=request.user.username)
        except:
            User = NewUser.objects.get(username=request.user.username)
        courses = User.course.all()
        if len(courses) > 0:
            try:
                course = courses.get(name=request.GET.get("course"))
            except:
                course = None
            if course is None:
                return render(
                    request,
                    "coursePage/register.html",
                    {
                        "course": request.GET.get("course"),
                        "duration": request.GET.get("duration"),
                    },
                )
            else:
                return redirect("/userPortal")
        else:
            return render(
                request,
                "coursePage/register.html",
                {
                    "course": request.GET.get("course"),
                    "duration": request.GET.get("duration"),
                },
            )
    request.session["next"] = (
        "/coursePage/register?course="
        + request.GET.get("course")
        + "&duration="
        + request.GET.get("duration")
    )
    return redirect("/login")
