from django.shortcuts import render
from django.urls import reverse
from . import templates


# Create your views here.


def index(request):
    return render(request, "partyPage/index.html", {})
