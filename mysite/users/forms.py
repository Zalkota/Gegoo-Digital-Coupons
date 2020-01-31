from django import forms
from .models import Profile

from allauth.account.forms import SignupForm
from django import forms
from users import models as users_models
from users import views as users_views


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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.layout = Layout(
    #         Row(
    #             Column('first_name', css_class='form-group col-md-6 mb-0'),
    #             Column('last_name', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Submit('submit', 'Sign in')
    #     )

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





# <**************************************************************************>
# <*****                      Merchant Approval Forms                   *****>
# <**************************************************************************>

class MerchantProfileForm(forms.ModelForm):
    class Meta:
       model = users_models.MerchantProfile
       fields = [
           'street_address',
           'city',
           'state',
           'zip',
           'phone_number',
           'website_url',
           'facebook_url',
       ]

    def __init__(self, *args, **kwargs):
        super(MerchantProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        #self.helper.form_id = 'id-exampleForm'
        #elf.helper.form_class = 'blueForms'
        self.helper.form_action = 'Submit'
        self.helper.layout = Layout(
            #Div('first_name', style="background: white;", title="Explication title", css_class="bigdivs")
            Field(
                Div(
                'business_name',
                css_class="col-lg-12 pb-4"
                ),
                Div(
                'description',
                css_class="col-lg-12 pb-4"
                ),
                Div(
                'street_address',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                'city',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                'state',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                'zip',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                'phone_number',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                'website_url',
                css_class="col-lg-12"
                ),
                Div(
                'facebook_url',
                css_class="col-lg-12"
                ),

        ),
    )
