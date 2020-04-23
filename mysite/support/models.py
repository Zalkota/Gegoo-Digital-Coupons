from django.db import models
from django.utils import timezone
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

class Topic(models.Model):
    title       = models.CharField(max_length=25, verbose_name='Title')
    slug        = models.SlugField(max_length=100)
    body        = models.TextField(blank=True, null=True)
    created_at  = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at  = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('support:topic_detail', kwargs={'slug': self.slug})

class Question(models.Model):

    STATUS_CHOICES = {
        ('DR', 'Draft'),
        ('PB', 'Published'),
    }

    title       = models.CharField(max_length=100)
    topic       = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    slug        = models.SlugField(max_length=100)
    # author      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='support_post')
    body        = models.TextField()
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DR')
    created_at  = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at  = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('support:question_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=Question)
def pre_save(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug



class Contact(models.Model):
    REASON_CHOICES = (
        ("QT", "I have a Question"),
        ("DS", "Dissatisfied with a Coupon"),
        ("BM", "I Would Like to post my own Coupons"),
        )

    reason = models.CharField(choices=REASON_CHOICES, default='QT', max_length=100)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = PhoneNumberField(null=True, blank=True)   #USE THIS https://github.com/stefanfoulis/django-phonenumber-field\
    description = models.TextField()
