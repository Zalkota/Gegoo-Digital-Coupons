from django import forms
from .models import Review
#from django.forms import ModelForm
#from .models import Contact

# Customize Crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Field, Div
from django.utils.safestring import mark_safe
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('__all__')
        widgets = {'review_user': forms.HiddenInput(), 'review_course': forms.HiddenInput(), 'summary':  forms.Textarea}


class AppointmentForm(forms.Form):

    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    TYPE_CHOICES = (
        (One, ''),
        (Two, ''),
        (Three, ''),
        (Four, ''),
        (Five, ''),
        (Six, ''),
        (SEVEN, ''),
        (EIGHT, ''),
        (NINE, ''),
        (TEN, ''),
        (ELEVEN, ''),
        (TWELVE, ''),
    )
    appointment_time = forms.ChoiceField(
            choices=TYPE_CHOICES,
            label="Appointment times",
            widget=forms.RadioSelect,
            required=True,
             )
    First_name = forms.CharField(required=True)
    Last_name = forms.CharField(label='Last Name', required=True)
    Email = forms.EmailField(required=True)
    Company = forms.CharField(label='Company', required=True)

def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        today = datetime.date.today()
        self.helper = FormHelper()
        #self.helper.form_id = 'id-exampleForm'
        #elf.helper.form_class = 'blueForms'
        self.helper.layout = Layout(
            #Div('first_name', style="background: white;", title="Explication title", css_class="bigdivs")
            Field(
            Div(
            HTML("<h5>{{ today }}<h5>"),
            'reservation_time',
            css_class="col-lg-6 test",

            ),
            Div(
                Div(
                'first_name',
                css_class="col-lg-6 px-4"
                ),
                Div(
                'last_name',
                css_class="col-lg-6 px-4"
                ),
                Div(
                'email',
                css_class="col-lg-6 px-4"
                ),
            css_class="row"
        ),
    )
)
