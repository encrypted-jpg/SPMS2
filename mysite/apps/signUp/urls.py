from django.urls import path

from . import views

app_name = "signUp"
urlpatterns = [
    path("", views.index, name="index"),
]
