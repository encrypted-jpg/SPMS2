from django.urls import path

from . import views

app_name = "userPortal"
urlpatterns = [
    path("", views.index, name="index"),
    path("slots/", views.slots, name="slots"),
    path("availableSlots/", views.availableSlots, name="availableSlots"),
    path("registrationPage/", views.registrationPage, name="registrationPage"),
    path("confirmMembership/", views.confirmMembership, name="confirmMembership"),
    path("course/", views.course, name="course"),
    path("comp/", views.comp, name="comp"),
    path("event/", views.event, name="event"),
]
