from django import forms
from .models import Profile
#For custom additional info required on signup, use this form and add this to settings.py

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Voornaam')
    last_name = forms.CharField(max_length=30, label='Achternaam')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "school"]
