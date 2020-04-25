from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import os
from portal.models import Store
from datetime import date
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib import messages
from django.shortcuts import reverse

# random_string_generator
import random
import string
def random_string_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



# ***************** VIDEO UPLOAD ***************************************************

def update_filename(instance, filename):
    slug = instance.store.slug
    today = datetime.now()
    time_string = today.strftime("%m-%d-%Y")
    path = slug + "/store-videos/" + time_string + '/'
    # time_string = str(today)
    format = filename
    return os.path.join(path, format)

# def ValidationResponse():
#     data = {'is_valid': False}
#     return JsonResponse(data)

def file_size(value): # add this to some file where you can import it from
    limit = 50 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(('File size too large, video must be under 10 MB'))


class VideoFile(models.Model):
    title           = models.CharField(max_length=255, blank=True, null=True)
    store           = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='videofile', null=True)
    file            = models.FileField(upload_to=update_filename, max_length=255, validators=[FileExtensionValidator(['mp4', 'mov']), file_size], help_text="Image must be a .MP4 or .MOV")
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    slug            = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return '%s' % (self.slug)

    def get_absolute_url(self):
        return reverse('users:merchant_video_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=VideoFile)
def pre_save_videofile(sender, **kwargs):
    print('pre_save_videofile')
    slug = slugify(kwargs['instance'].store.slug, kwargs['instance'].uploaded_at)
    kwargs['instance'].slug = slug
    kwargs['instance'].title = kwargs['instance'].file.name

# *************** IMAGE UPLOAD *******************************************************


def update_image_filename(instance, filename):
    slug = instance.store.slug
    today = datetime.now()
    time_string = today.strftime("%m-%d-%Y")
    path = slug + "/store-images/" + time_string + '/'
    # time_string = str(today)
    format = filename
    return os.path.join(path, format)

# def ValidationResponse():
#     data = {'is_valid': False}
#     return JsonResponse(data)

def image_size(value): # add this to some file where you can import it from
    limit = 3 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(('File size too large, image must be under 3 MB'))


class ImageFile(models.Model):
    title           = models.CharField(max_length=255, blank=True, null=True)
    store           = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='imagefile', null=True)
    file            = models.FileField(upload_to=update_image_filename, max_length=255, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), image_size], help_text="Image must be a .JPG, PNG, or .JPEG")
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    slug            = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return '%s' % (self.slug)

    def get_absolute_url(self):
        return reverse('users:merchant_image_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=ImageFile)
def pre_save_image_file(sender, **kwargs):
    random_number = random_string_generator()
    today = datetime.now()
    string = str(today) + '-' + str(random_number)
    slug = slugify(string)
    kwargs['instance'].slug = slug
    kwargs['instance'].title = kwargs['instance'].file.name


# ***************** FILE UPLOAD ***************************************************

def update_downloadable_filename(instance, filename):
    slug = instance.store.slug
    today = datetime.now()
    time_string = today.strftime("%m-%d-%Y")
    path = slug + "/store-files/" + time_string + '/'
    # time_string = str(today)
    format = filename
    return os.path.join(path, format)


class DownloadableFile(models.Model):
    title           = models.CharField(max_length=255, blank=True, null=True)
    store           = models.OneToOneField(Store, on_delete=models.CASCADE, related_name='downloadablefile', null=True)
    file            = models.FileField(upload_to=update_downloadable_filename, max_length=255, validators=[FileExtensionValidator(['pdf', 'zip', 'ppt', 'pptx']), file_size], help_text="File must be PDF, ZIP, or PowerPoint")
    uploaded_at     = models.DateTimeField(auto_now_add=True)
    slug            = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return '%s' % (self.slug)

    def get_absolute_url(self):
        return reverse('users:merchant_file_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=DownloadableFile)
def pre_save_downloadablefile(sender, **kwargs):
    slug = slugify(kwargs['instance'].store.slug, kwargs['instance'].uploaded_at)
    kwargs['instance'].slug = slug
    kwargs['instance'].title = kwargs['instance'].file.name
