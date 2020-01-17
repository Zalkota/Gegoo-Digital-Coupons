from django import forms
import datetime
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import SelectDateWidget
from django.forms.fields import DateField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from portal import models as portal_models


# Customize Crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Field, Div
from django.utils.safestring import mark_safe
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions, StrictButton)


class MerchantStoreForm(forms.ModelForm):
    class Meta:
       model = portal_models.Store
       fields = 'business_name', 'description', 'category', 'subcategory', 'street_address', 'city', 'state', 'zip', 'phone_number', 'code_coupon', 'website_url', 'facebook_url', 'logo',


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
                'business_name',
                css_class="col-lg-12 pb-4"
                ),
                Div(
                'description',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                'category',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                'subcategory',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                'street_address',
                css_class="col-lg-6"
                ),
                Div(
                'city',
                css_class="col-lg-6"
                ),
                Div(
                'state',
                css_class="col-lg-6"
                ),
                Div(
                'zip',
                css_class="col-lg-6"
                ),
                Div(
                'phone_number',
                css_class="col-lg-6"
                ),
                Div(
                'code_coupon',
                css_class="col-lg-6"
                ),
                Div(
                'website_url',
                css_class="col-lg-6"
                ),
                Div(
                'facebook_url',
                css_class="col-lg-6"
                ),
                Div(
                'logo',
                css_class="col-lg-6"
                ),

        ),
    )
