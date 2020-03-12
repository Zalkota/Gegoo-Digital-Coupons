from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import reverse
import decimal

import stripe
import datetime

from users import models as users_models

from payments.functions import unique_coupon_generator

class Benefit(models.Model):
	description = models.CharField(max_length=36, help_text="Describe a benefit of the subscription product.")

	def __str__(self):
		return self.description

class Plan(models.Model):
    slug        = models.CharField(max_length=100, blank=True)
    nickname    = models.CharField(max_length=50, blank=True, editable=False)
    product_id  = models.CharField(max_length=50, blank=True, editable=False)
    plan_id     = models.CharField(max_length=50, blank=True)
    amount      = models.DecimalField(default=0, validators=[MinValueValidator(0)], decimal_places=2, max_digits=10)
    currency    = models.CharField(max_length=50, blank=True, editable=False)
    interval    = models.CharField(max_length=50, blank=True, editable=False)
    description = models.CharField(max_length=255, default="add description")
    benefit = models.ManyToManyField(Benefit)

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse('payments:plan_detail', kwargs={'slug': self.slug})

    def get_total(self):
        return self.amount / decimal.Decimal(100)
        total = property(stripe_total)

    @property
    def all_benefits(self):
        return self.benefit.all()

@receiver(pre_save, sender=Plan)
def pre_save_plan(sender, instance, **kwargs):
    stripe.api_key              = settings.STRIPE_SECRET_KEY
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
    latest_invoice_status       = models.CharField(max_length=100, blank=True)
    payment_status              = models.CharField(max_length=100, blank=True)
    unix_trial_start            = models.PositiveIntegerField(blank=True, null=True)
    unix_trial_end              = models.PositiveIntegerField(blank=True, null=True)
    trial_start                 = models.DateTimeField(blank=True, null=True)
    trial_end                   = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.subscription_id

    def get_absolute_url(self):
        return reverse('payments:subscription_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=Subscription)
def pre_save_subscription(sender, instance, **kwargs):
    slug                        = slugify(instance.subscription_id)
    instance.slug               = slug

    if instance.unix_trial_start is not None and instance.unix_trial_end is not None:
        unix_timestamp_start        = instance.unix_trial_start
        unix_timestamp_end          = instance.unix_trial_end
        trial_start_date            = datetime.datetime.fromtimestamp(unix_timestamp_start)
        trial_end_date              = datetime.datetime.fromtimestamp(unix_timestamp_end)
        instance.trial_start        = trial_start_date
        instance.trial_end          = trial_end_date

class Promotion(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=50, unique=True, blank=True)
    trial_period = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField(default=timezone.now, verbose_name="Valid From")
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code

@receiver(pre_save, sender=Promotion)
def pre_save_coupon(sender, **kwargs):
    if kwargs['instance'].code is None or kwargs['instance'].code == "":
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
