from django import forms

# Customize Crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div, Button, Field

class PromotionForm(forms.Form):
    code = forms.CharField(label='Code', max_length=50)

    def __init__(self, *args, **kwargs):
        super(PromotionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(Field('code', placeholder='Promotional Code'), css_class='col-md-12 mb-0'),
                Column(
                    Submit('submit', 'Apply', css_class="btn btn-primary-alt py-2 btn-block w-100",),
                    css_class='col-md-12 mb-0'
                ),
                css_class='row'
            ),
        )
        self.helper.form_show_labels = False
