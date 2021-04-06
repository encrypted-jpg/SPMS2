from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from mysite.models import *


# Create your views here.
def compute_comp(
    id,
):  # It computes the from_age and to_age of a Competition based on the games in it
    comp = Competition.objects.get(id=id)
    low = 100
    high = 0
    for x in comp.game_set.all():
        if x.from_age <= low:
            low = x.from_age
        if x.to_age >= high:
            high = x.to_age
    comp.from_age = low
    comp.to_age = high


def calculateAge(birthDate):  # Returns the Age from DOB
    today = date.today()
    age = (
        today.year
        - birthDate.year
        - ((today.month, today.day) < (birthDate.month, birthDate.day))
    )
    return age


def index(
    request,
):  # Returns the Competition list and games list to display in the site
    comp = Competition.objects.all()
    lst = []
    for x in comp:
        pst = [x]
        kst = []
        if len(x.game_set.all()) > 6:
            for y in x.game_set.all()[:6]:
                kst.append(y.game_type)
        else:
            for y in x.game_set.all():
                kst.append(y.game_type)
        pst.append(tuple(kst))
        s = Compslot.objects.filter(competition=x)[0]
        pst.append(s)
        lst.append(tuple(pst))
    context = {"data": lst}
    return render(request, "compPage/index.html", context=context)


def participate(request):
    if request.user is not None and request.user.username is not "":
        user = NewUser.objects.filter(username=request.user.username)[0]
        if (
            user.type == "MANAGER"
        ):  # Redirects to Manager Competition page if the User is a Manager
            messages.add_message(
                request,
                messages.INFO,
                "You are a Manager!! This Functionality is Working Properly..",
                extra_tags="custom",
            )
            return redirect("/userPortal/comp/")
        if request.method == "POST":
            id = request.session["comp_id"]
            del request.session["comp_id"]
            user = NewUser.objects.filter(username=request.user.username)[0]
            comp = Competition.objects.filter(id=id)[0]
            pst = request.POST.get("game_lst").split("-$-")
            for x in comp.game_set.all():
                if x.game_type in pst:
                    gslot = Gameslot.objects.filter(game=x)[0]
                    gslot.users.add(user)
                    gslot.rem_num_participants -= 1
                    gslot.save()
            user.comp_participated += 1
            user.comp_cert = request.FILES[
                "cert"
            ]  # Retrieves Data from the form and enrolls the user in the
            user.comp_count += 1  # Corresponding Games
            user.save()
            messages.add_message(
                request,
                messages.INFO,
                "You are successfully enrolled in the competition " + comp.name,
                extra_tags="custom",
            )
            return redirect("/userPortal/comp/")
        if request.method == "GET" and request.GET.get("comp") is not None:
            comp = Competition.objects.filter(id=request.GET.get("comp"))[0]
            user = NewUser.objects.filter(username=request.user.username)[0]
            for game in comp.game_set.all():
                if (
                    user in Gameslot.objects.filter(game=game)[0].users.all()
                ):  # Checks for Enrollment Status
                    messages.add_message(
                        request,
                        messages.INFO,
                        "You are already enrolled in the competition " + comp.name,
                        extra_tags="custom",
                    )
                    return redirect("/userPortal/comp")
            lst = []
            compute_comp(comp.id)
            age = calculateAge(user.age)
            for x in comp.game_set.all():  # Applying Gender Filter
                if (
                    x.gender == "Both"
                    or x.gender
                    == NewUser.objects.filter(username=request.user.username)[0].gender
                    and (x.from_age <= age <= x.to_age)
                ):
                    s = Gameslot.objects.get(game=x)
                    if s.rem_num_participants > 0:
                        lst.append((x, s))
            context = {"comp_name": comp.name, "game_lst": lst}
            request.session["comp_id"] = comp.id
            return render(request, "compPage/participate.html", context=context)
        return render(request, "compPage/participate.html", {})
    else:
        request.session["next"] = "/compPage/participate?comp=" + str(
            request.GET.get("comp")
        )
        return redirect("/login")


def ticket(request):
    if request.user is not None and request.user.username is not "":
        user = NewUser.objects.filter(username=request.user.username)[0]
        if user.type == "MANAGER":  # Check if the User is a Manager
            messages.add_message(
                request,
                messages.INFO,
                "You are a Manager!! This Functionality is Working Properly..",
                extra_tags="custom",
            )
            return redirect("/userPortal/comp")
        if request.method == "POST":
            id = request.session["comp_id"]
            del request.session["comp_id"]
            User = NewUser.objects.filter(username=request.user.username)[0]
            comp = Competition.objects.filter(id=id)[0]
            tkt = Ticket(
                num_tickets=request.POST.get("num")
            )  # Add a Ticket to the User
            tkt.save()
            tkt.user.add(User)
            tkt.competition.add(comp)
            tkt.save()
            cslot = Compslot.objects.filter(competition=comp)[0]
            cslot.users.add(User)
            cslot.save()
            messages.add_message(
                request,
                messages.INFO,
                "A ticket is successfully booked!!",
                extra_tags="custom",
            )
            return redirect("/userPortal/comp")
        if request.method == "GET":
            comp = Competition.objects.filter(id=request.GET.get("comp"))[0]
            try:
                User = NewUser.objects.filter(username=request.user.username)[0]
            except:
                User = NewUser.objects.filter(username=request.user.username)[0]
            id = comp.id  # Checking if the User has already a Ticket
            if (
                len(
                    Ticket.objects.filter(
                        user=User, competition=Competition.objects.filter(id=id)[0]
                    )
                )
                > 0
            ):
                messages.add_message(
                    request,
                    messages.INFO,
                    "You Already have a Ticket for the competition " + comp.name,
                    extra_tags="custom",
                )
                return redirect("/userPortal/comp")
            context = {"comp_name": comp.name}
            request.session["comp_id"] = comp.id
            return render(request, "compPage/ticket.html", context=context)
        return render(request, "compPage/ticket.html", {})
    else:
        return redirect("/login")
