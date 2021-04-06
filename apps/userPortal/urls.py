from django.urls import path

from . import views

app_name = "userPortal"
urlpatterns = [
    path("", views.index, name="index"),
    path("availableSlots/", views.availableSlots, name="availableSlots"),
    path("registrationPage/", views.registrationPage, name="registrationPage"),
    path("confirmMembership/", views.confirmMembership, name="confirmMembership"),
    path("course/", views.course, name="course"),
    path("comp/", views.comp, name="comp"),
    path("event/", views.event, name="event"),
    path("managerCreateCourse/", views.managerCreateCourse, name="managerCreateCourse"),
    path("managerCreateComp/", views.managerCreateComp, name="managerCreateComp"),
    path("managerCreateGame/", views.managerCreateGame, name="managerCreateGame"),
    path(
        "coordinatorCoursePage/",
        views.coordinatorCoursePage,
        name="coordinatorCoursePage",
    ),
    path("courseSlotRegister/", views.courseSlotRegister, name="courseSlotRegister"),
    path("suggestion/", views.suggestion, name="suggestion"),
]
