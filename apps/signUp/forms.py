from django import forms
from django.contrib.auth.forms import UserCreationForm

from mysite.models import NewUser


class DateInput(forms.DateInput):
    input_type = "date"


class CreateUserForm(UserCreationForm):
    age = forms.DateField(widget=DateInput)
    gender = forms.CharField(max_length=100)
    city = forms.CharField(max_length=15)
    country = forms.CharField(max_length=20)

    class Meta:
        model = NewUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "age",
            "gender",
            "email",
            "city",
            "country",
            "password1",
            "password2",
        ]
