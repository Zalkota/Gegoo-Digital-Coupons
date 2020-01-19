from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify

from django.shortcuts import reverse

import stripe

class Plan(models.Model):
    slug        = models.CharField(max_length=100, blank=True)
    nickname    = models.CharField(max_length=50, blank=True)
    product_id  = models.CharField(max_length=50, blank=True)
    plan_id     = models.CharField(max_length=50, blank=True)
    amount      = models.CharField(max_length=50, blank=True)
    currency    = models.CharField(max_length=50, blank=True)
    interval    = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse('payments:plan_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=Plan)
def pre_save_product(sender, instance, **kwargs):
    stripe.api_key              = settings.STRIPE_SECRET_KEY_MPM
    plan                        = stripe.Plan.retrieve(id=instance.plan_id)
    instance.nickname           = plan['nickname']
    instance.product_id         = plan['product']
    instance.amount             = plan['amount']
    instance.currency           = plan['currency']
    instance.interval           = plan['interval']

    slug                        = slugify(instance.nickname)
    instance.slug               = slug

class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    subscription_id     = models.CharField(max_length=50, blank=True)
    subscription_status = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.subscription_id
