from django.db import models
from datetime import date
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
#get_absolute_url
from django.urls import reverse
from django.utils.text import slugify
#Ckeditor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


@python_2_unicode_compatible
class BaseModel(models.Model):
    #TODO: Add queryset managers / mixins
    is_active = models.BooleanField(default=True, help_text=('Designates whether this item should be treated as active. Unselect this instead of deleting data.'), db_index=True) #TODO: Can I hide this on the model form unless user has permissions or do I do this in forms.py? Change these to 'visible' or 'is_active'??
    created_time = models.DateTimeField(('created time'), editable=False, auto_now_add=True, blank=True, null=True)
    modified_time = models.DateTimeField(('last modified time'), editable=False, auto_now=True)
    #  id = models.BigAutoField(primary_key=True)
    class Meta:
        abstract = True
