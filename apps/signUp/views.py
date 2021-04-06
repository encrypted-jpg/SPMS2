from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import CreateUserForm


# Create your views here.


def index(request):
    if (
        request.user is not None and request.user.username is not ""
    ):  # If the User is already logged in it redirects to UserPortal
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
        if form.is_valid():  # Validation of submitted Form
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(
                request, new_user
            )  # Get's the Data from the form if it is valid and logins the user
            try:
                if request.session["next"]:
                    url = request.session["next"]
                    del request.session["next"]
                    return redirect(url)
            except:
                return redirect("/userPortal")

    context = {"form": form}
    return render(request, "signUp/index.html", context=context)
