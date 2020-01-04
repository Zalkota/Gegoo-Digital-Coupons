from django import forms
from portal.models import Address

from allauth.account.forms import SignupForm
from django import forms
from users.models import User


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
    city_input = forms.CharField(label="City, State", initial='Explore coupons in what city?',required=True, widget=forms.TextInput(attrs={
        'style': 'display: none;',
    }))

    state_input = forms.CharField(label="City, State", initial='Explore coupons in what city?',required=True, widget=forms.TextInput(attrs={
        'style': 'display: none;',
    }))


class MerchantSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        user = super(MerchantSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_merchant = True
        user.is_active = True
        user.save()
        return user

# class ConsumerSignupForm(SignupForm):
#     def save(self, request):
#         user = super(ConsumerSignupForm, self).save(request)
#         user.is_consumer = True
#         user.is_active = True
#         user.save()
#         return user
