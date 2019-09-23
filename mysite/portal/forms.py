from django import forms
from .models import Review, Job

import datetime
from .models import Job, Image
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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('__all__')
        widgets = {'review_user': forms.HiddenInput(), 'review_course': forms.HiddenInput(), 'summary':  forms.Textarea}

class JobForm(forms.ModelForm):
    
    class Meta:
       model = Job
       fields = ['description', 'desired_plants', 'hardscaping', 'hardscaping_description', 'due_date']

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        #self.helper.form_id = 'id-exampleForm'
        #elf.helper.form_class = 'blueForms'
        self.helper.layout = Layout(
            #Div('first_name', style="background: white;", title="Explication title", css_class="bigdivs")
            Field(
            Div(
                Div(
                'description',
                css_class="col-lg-6 px-4"
                ),
                Div(
                'desired_plants',
                css_class="col-lg-4 px-4"
                ),
                Div(
                'hardscaping',
                css_class="col-lg-4 px-4"
                ),
                Div(
                'hardscaping_description',
                css_class="col-lg-4 px-4"
                ),
                Div(
                'due_date',
                css_class="col-lg-4 px-4"
                ),
            css_class="row px-4 py-4 text-left"
        ),
    )
)


class ImageForm(forms.ModelForm):
    class Meta:
       model = Image
       fields = ['file']
