from django import forms
import datetime
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import SelectDateWidget
from django.forms.fields import DateField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from portal import models as portal_models

from portal.fields import GroupedModelChoiceField

# Customize Crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Field, Div
from django.utils.safestring import mark_safe
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions, StrictButton)




class MerchantStoreForm(forms.ModelForm):
    subcategory = GroupedModelChoiceField(queryset=portal_models.Subcategory.objects.all(), choices_groupby='category')

    class Meta:
       model = portal_models.Store
       fields = [
       'business_name',
       'slogan',
       'description',
       # 'category',
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
        super(MerchantStoreForm, self).__init__(*args, **kwargs)

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
                # 'category',
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



class MerchantTestimonialForm(forms.ModelForm):
    class Meta:
       model = portal_models.Testimonial
       fields = [

       'title',
       'review',
       'rating',
       ]


    def __init__(self, *args, **kwargs):
        super(MerchantTestimonialForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        #self.helper.form_id = 'id-exampleForm'
        #elf.helper.form_class = 'blueForms'
        self.helper.form_action = 'Submit'
        self.helper.layout = Layout(
            Field(
                Div(
                'title',
                'review',
                'rating',
                css_class="col-lg-12 pb-4"
                ),
            ),
    )
