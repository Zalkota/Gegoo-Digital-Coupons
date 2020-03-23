from django import forms
from .models import Profile

from allauth.account.forms import SignupForm
from django import forms
from users import models as users_models
from users import views as users_views

from portal import models as portal_models

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

class MerchantApprovalStoreForm(forms.ModelForm):
    class Meta:
       model = portal_models.Store
       fields = [
       'business_name',
       'slogan',
       'description',
       'category',
       'subcategory',
       'street_address',
       'city',
       'state',
       'zip',
       'phone_number',
       'code_coupon',
       'website_url',
       'facebook_url',
       'logo',
       'id',
       ]


    def __init__(self, *args, **kwargs):
        super(MerchantApprovalStoreForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        #self.helper.form_id = 'id-exampleForm'
        #elf.helper.form_class = 'blueForms'
        self.helper.form_action = 'Submit'
        self.helper.layout = Layout(
            #Div('first_name', style="background: white;", title="Explication title", css_class="bigdivs")
            Field(
                Div(
                    HTML("<h3 class='subheader text-uppercase text-gray-700 fs-16 mb-2'>Basic Info<h3>"),
                    HTML("<p class='text-secondary fs-14'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.<p>"),
                css_class="col-lg-6"
                ),
                Div(
                'business_name',
                'category',
                'subcategory',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                    HTML("<hr>"),
                css_class="col-lg-12"
                ),
                Div(
                    HTML("<h3 class='subheader text-uppercase text-gray-700 fs-16 mb-2'>Address<h3>"),
                    HTML("<p class='text-secondary fs-14'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.<p>"),
                css_class="col-lg-6"
                ),
                Div(
                'street_address',
                'city',
                'state',
                'zip',
                'phone_number',
                css_class="col-lg-6"
                ),
                Div(
                    HTML("<hr>"),
                css_class="col-lg-12"
                ),
                Div(
                    HTML("<h3 class='subheader text-uppercase text-gray-700 fs-16 mb-2'>Marketing<h3>"),
                    HTML("<p class='text-secondary fs-14'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.<p>"),
                css_class="col-lg-6"
                ),
                Div(
                'code_coupon',
                'slogan',
                'description',
                'website_url',
                'facebook_url',
                    Div(
                    'logo',
                    css_class="custom-input-button"
                    ),
                css_class="col-lg-6"
                ),

                Div(
                    HTML("<hr>"),
                css_class="col-lg-12"
                ),
                # Div(
                #     Submit('Save', 'Create Store', css_class='btn btn-primary-alt btn-block mt-3 pull-right'),
                # css_class="col-lg-12"
                # ),
            ),
    )

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
#
# class MerchantProfileForm(forms.ModelForm):
#     class Meta:
#        model = users_models.MerchantProfile
#        fields = [
#         'business_name',
#            'street_address',
#            'city',
#            'state',
#            'zip',
#            'phone_number',
#            'website_url',
#            'facebook_url',
#        ]
#
#     def __init__(self, *args, **kwargs):
#         super(MerchantProfileForm, self).__init__(*args, **kwargs)
#
#         self.helper = FormHelper()
#         #self.helper.form_id = 'id-exampleForm'
#         #elf.helper.form_class = 'blueForms'
#         self.helper.form_action = 'Submit'
#         self.helper.layout = Layout(
#             #Div('first_name', style="background: white;", title="Explication title", css_class="bigdivs")
#             Field(
#                 Div(
#                 'business_name',
#                 css_class="col-lg-12 pb-4"
#                 ),
#                 Div(
#                 'street_address',
#                 css_class="col-lg-6 pb-4"
#                 ),
#                 Div(
#                 'city',
#                 css_class="col-lg-6 pb-4"
#                 ),
#                 Div(
#                 'state',
#                 css_class="col-lg-6 pb-4"
#                 ),
#                 Div(
#                 'zip',
#                 css_class="col-lg-6 pb-4"
#                 ),
#                 Div(
#                 'phone_number',
#                 css_class="col-lg-6 pb-4"
#                 ),
#
#         ),
#     )
