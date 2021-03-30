from django.urls import path

from . import views

app_name = "partyPage"
urlpatterns = [path("", views.index, name="index")]
