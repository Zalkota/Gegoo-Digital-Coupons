from django import forms

import datetime
from .models import VideoFile, ImageFile, DownloadableFile
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


class VideoFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
    class Meta:
       model = VideoFile
       fields = ['file']


class ImageFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
    class Meta:
       model = ImageFile
       fields = ['file']

class DownloadableFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
    class Meta:
       model = DownloadableFile
       fields = ['file']
