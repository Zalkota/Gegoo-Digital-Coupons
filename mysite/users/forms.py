from django import forms
from .models import Profile
#For custom additional info required on signup, use this form and add this to settings.py

MERCHANT_SELECT = (
    ("NO", "No"),
    ("YES", "Yes")
    )


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Voornaam')
    last_name = forms.CharField(max_length=30, label='Achternaam')
    merchant_select = forms.ChoiceField(choices=MERCHANT_SELECT, default='NO', max_length=2)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.merchant_select = self.cleaned_data['merchant_select']
        user.save()

# class ProfileImageForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ["image"]
