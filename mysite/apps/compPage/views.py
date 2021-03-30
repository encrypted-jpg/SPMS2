from django.shortcuts import render, redirect
from django.urls import reverse
from . import templates
from .models import Competition, Game, Ticket
from mysite.models import *
from datetime import date, datetime


# Create your views here.
def compute_comp(id):
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


def calculateAge(birthDate):
    today = date.today()
    age = (
        today.year
        - birthDate.year
        - ((today.month, today.day) < (birthDate.month, birthDate.day))
    )
    return age


def index(request):
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
            user.comp_cert = request.FILES["cert"]
            user.save()
            return redirect("/userPortal")
        if request.method == "GET" and request.GET.get("comp") is not None:
            comp = Competition.objects.filter(id=request.GET.get("comp"))[0]
            user = NewUser.objects.filter(username=request.user.username)[0]
            for game in comp.game_set.all():
                if user in Gameslot.objects.filter(game=game)[0].users.all():
                    return redirect("/userPortal")
            lst = []
            compute_comp(comp.id)
            age = calculateAge(user.age)
            for x in comp.game_set.all():
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
        if request.method == "POST":
            id = request.session["comp_id"]
            del request.session["comp_id"]
            User = NewUser.objects.filter(username=request.user.username)[0]
            comp = Competition.objects.filter(id=id)[0]
            tkt = Ticket(num_tickets=request.POST.get("num"))
            tkt.save()
            tkt.user.add(User)
            tkt.competition.add(comp)
            tkt.save()
            cslot = Compslot.objects.filter(competition=comp)[0]
            cslot.users.add(User)
            cslot.save()
            return redirect("/userPortal")
        if request.method == "GET":
            comp = Competition.objects.filter(id=request.GET.get("comp"))[0]
            try:
                User = NewUser.objects.filter(username=request.user.username)[0]
            except:
                User = NewUser.objects.filter(username=request.user.username)[0]
            id = comp.id
            if (
                len(
                    Ticket.objects.filter(
                        user=User, competition=Competition.objects.filter(id=id)[0]
                    )
                )
                > 0
            ):
                return redirect("/userPortal")
            context = {"comp_name": comp.name}
            request.session["comp_id"] = comp.id
            return render(request, "compPage/ticket.html", context=context)
        return render(request, "compPage/ticket.html", {})
    else:
        return redirect("/login")
