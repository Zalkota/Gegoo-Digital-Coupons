from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import reverse

import stripe

from payments.functions import unique_coupon_generator

class Benefit(models.Model):
	description = models.CharField(max_length=36, help_text="Describe a benefit of the subscription product.")

	def __str__(self):
		return self.description

class Plan(models.Model):
    slug        = models.CharField(max_length=100, blank=True, editable=False)
    nickname    = models.CharField(max_length=50, blank=True, editable=False)
    product_id  = models.CharField(max_length=50, blank=True, editable=False)
    plan_id     = models.CharField(max_length=50, blank=True)
    amount      = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    currency    = models.CharField(max_length=50, blank=True, editable=False)
    interval    = models.CharField(max_length=50, blank=True, editable=False)
    description = models.CharField(max_length=255, default="add description")
    benefit = models.ManyToManyField(Benefit)

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse('payments:plan_detail', kwargs={'slug': self.slug})

    def get_total(self):
        return int(self.amount) / 100.00
        total = property(stripe_total)

    @property
    def all_benefits(self):
        return self.benefit.all()

@receiver(pre_save, sender=Plan)
def pre_save_plan(sender, instance, **kwargs):
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
    user                        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='subscription')
    slug                        = models.CharField(max_length=100, blank=True)
    subscription_id             = models.CharField(max_length=50, blank=True)
    subscription_quantity       = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    subscription_item_id        = models.CharField(max_length=50, blank=True, editable=False)
    plan_id                     = models.CharField(max_length=50, blank=True)
    subscription_status         = models.CharField(max_length=50, blank=True, editable=False)

    def __str__(self):
        return self.subscription_id

    def get_absolute_url(self):
        return reverse('payments:subscription_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=Subscription)
def pre_save_subscription(sender, instance, **kwargs):
    slug            = slugify(instance.subscription_id)
    instance.slug   = slug

class Promotion(models.Model):
    code = models.CharField(max_length=50, unique=True, blank=True)
    trial_period = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField(default=timezone.now, verbose_name="Valid From")
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code
    
@receiver(pre_save, sender=Promotion)
def pre_save_coupon(sender, **kwargs):
    if kwargs['instance'].code == None or kwargs['instance'].code == "":
        p_code = str(unique_coupon_generator())
        promo = 'PROMO'
        promo_code = promo + p_code
        kwargs['instance'].code = promo_code


class PromoUser(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='promo_user')
    promotion   = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True, related_name='promo')
    has_used    = models.BooleanField(default=False)
    redeemd_at  = models.DateTimeField(default=timezone.now, verbose_name="Redeemed At")

    def __str__(self):
        return self.user.username
