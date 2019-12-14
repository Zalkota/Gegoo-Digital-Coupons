from django import forms
from .models import Profile
from portal.models import Address


# Customize Crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Field, Div
from django.utils.safestring import mark_safe
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions, StrictButton)

RETURN_CHOICES = (
    ('F', 'Found a better deal'),
    ('S', 'Not satisfied with the quality'),
    ('T', 'Took too long to arrive'),
    ('N', 'None of the above')
)

class userLocationForm(forms.Form):
    location_input = forms.CharField(label="City, State", initial='Explore coupons in what city?',required=True, widget=forms.Select(choices=RETURN_CHOICES, attrs={
        'class': ' d-block w-100',
    }))
    # state = forms.CharField(widget=forms.Textarea(attrs={
    #     'rows': 4
    # }))





class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Voornaam')
    last_name = forms.CharField(max_length=30, label='Achternaam')
    # merchant_select = forms.ChoiceField(choices=MERCHANT_SELECT, default='NO', max_length=2)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.merchant_select = self.cleaned_data['merchant_select']
        user.save()

# class ProfileImageForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ["image"]
