from django.urls import path

from . import views

app_name = "coursePage"
urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.registration, name="register"),
]
