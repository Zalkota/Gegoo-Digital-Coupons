from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os
from datetime import date
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

class FileItem(models.Model):
    user                            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name                            = models.CharField(max_length=120, null=True, blank=True)
    path                            = models.TextField(blank=True, null=True)
    size                            = models.BigIntegerField(default=0)
    file_type                       = models.CharField(max_length=120, null=True, blank=True)
    timestamp                       = models.DateTimeField(auto_now_add=True)
    updated                         = models.DateTimeField(auto_now=True)
    uploaded                        = models.BooleanField(default=False)
    active                          = models.BooleanField(default=True)

    @property
    def title(self):
        return str(self.name)


def update_filename(instance, filename):
    path = "store-videos/"
    today = datetime.now()
    time_string = today.strftime("%m-%d-%Y %H:-%M:-%S")
    # time_string = str(today)
    format = instance.user.username + time_string
    return os.path.join(path, format)




class VideoFile(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title           = models.CharField(max_length=255, blank=True)
    file            = models.FileField(upload_to=update_filename, validators=[FileExtensionValidator(['mp4', 'mov'])], help_text="Image must be a .MP4 or .MOV")
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    slug            = models.SlugField(unique=True, blank=True, editable=False)

    def __str__(self):
        return '%s' % (self.file)

@receiver(pre_save, sender=VideoFile)
def pre_save_videofile(sender, **kwargs):
    slug = slugify(kwargs['instance'].file)
    kwargs['instance'].slug = slug
