from django import forms
import datetime
from .models import Contact
from portal.models import Address
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.widgets import SelectDateWidget
from django.forms.fields import DateField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _



# Customize Crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Field, Div
from django.utils.safestring import mark_safe
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions, StrictButton)


class ContactForm(forms.ModelForm):
    class Meta:
       model = Contact
       fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        #self.helper.form_id = 'id-exampleForm'
        #elf.helper.form_class = 'blueForms'
        self.helper.form_action = 'Submit'
        self.helper.layout = Layout(
            #Div('first_name', style="background: white;", title="Explication title", css_class="bigdivs")
            Field(
                Div(
                'reason',
                css_class="col-lg-12 pb-4"
                ),
                Div(
                'name',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                'email',
                css_class="col-lg-6 pb-4"
                ),
                Div(
                'description',
                css_class="col-lg-12"
                ),

        ),
    )




class ContactMiniForm(forms.ModelForm):
    class Meta:
       model = Contact
       fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ContactMiniForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        #self.helper.form_id = 'id-exampleForm'
        #elf.helper.form_class = 'blueForms'
        self.helper.form_action = 'Submit'
        self.helper.layout = Layout(
            #Div('first_name', style="background: white;", title="Explication title", css_class="bigdivs")
            Field(
            Div(
                Div(
                'name',
                css_class="col-lg-12"
                ),
                Div(
                'email',
                css_class="col-lg-12"
                ),
                Div(
                'phone',
                css_class="col-lg-12"
                ),
                Div(
                'description',
                css_class="col-lg-12"
                ),
                #Div(
                #StrictButton("Submit", name="submit", value="submit", type='submit', css_class='btn btn-primary-alt py-3 mt-3 px-5'),
                #css_class="col-lg-12"
                #),
            css_class="row px-4 py-4 text-left"
        ),
    )
)
