from django import forms
from .models import Membership_form
from phonenumber_field.formfields import PhoneNumberField


class UploadFileForm(forms.Form):
    aCardNum = forms.CharField(max_length=50)
    num_months = forms.ChoiceField(
        choices=((1, "1"), (3, "3"), (6, "6"), (9, "9"), (12, "12"))
    )
    phone_num = PhoneNumberField()
    file = forms.FileField()

    class Meta:
        model = Membership_form
        fields = ["aCardNum", "phone_num", "num_months", "file"]
