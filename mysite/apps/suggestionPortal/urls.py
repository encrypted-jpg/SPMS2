from django.urls import path

from . import views

app_name = "suggestionPortal"
urlpatterns = [
    path("", views.index, name="index"),
]
