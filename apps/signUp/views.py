from django.shortcuts import render, redirect
from django.urls import reverse
from . import templates
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login

# Create your views here.


def index(request):
    if request.user is not None and request.user.username is not "":
        try:
            if request.session["next"]:
                url = request.session["next"]
                del request.session["next"]
                return redirect(url)
        except:
            return redirect("/userPortal")
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            try:
                if request.session["next"]:
                    url = request.session["next"]
                    del request.session["next"]
                    return redirect(url)
            except:
                return redirect("/userPortal")

    context = {"form": form}
    return render(request, "signUp/index.html", context=context)
