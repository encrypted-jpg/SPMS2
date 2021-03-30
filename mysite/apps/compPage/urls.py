from django.urls import path

from . import views

app_name = "compPage"
urlpatterns = [
    path("", views.index, name="index"),
    path("participate", views.participate, name="participate"),
    path("ticket", views.ticket, name="ticket"),
]
