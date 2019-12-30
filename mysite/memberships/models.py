# <**************************************************************************>
# <*****                         IMPORTS                                *****>
# <**************************************************************************>

from django.conf import settings
from django.db import models
#mail
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.db.models.signals import post_save, post_init
import uuid
from datetime import datetime
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# <**************************************************************************>
# <*****                         MODELS                                 *****>
# <**************************************************************************>

class Benefit(models.Model):
	name = models.CharField(max_length=36)

	def __str__(self):
		return self.name

class Membership(models.Model):
	MEMBERSHIP_CHOICES = (
	('BM', 'Basic Advertising'),
	('PM', 'Premium Advertising'),
	)
	slug = models.SlugField()
	position = models.PositiveSmallIntegerField(null=True)
	membership_type = models.CharField(
			choices=MEMBERSHIP_CHOICES,
			default='Basic Advertising',
			max_length=30)
	benefit = models.ManyToManyField(Benefit)
	description = models.CharField(max_length=255, default="add description")
	price = models.PositiveIntegerField(default=0)
	stripe_price = models.PositiveIntegerField(default=0)
	tax = models.DecimalField(null=True, max_digits=6, decimal_places=2)
	stripe_plan_id = models.CharField(max_length=40)
	image = models.ImageField(null=True)

	#def get_total(self):
    #    return sum([item.product.price for item in self.tax])

	def get_total(self):
		return self.tax + self.price
		total = property(get_total)

	def stripe_total(self):
		return (self.tax + self.price) * 100
		total = property(stripe_total)

	def __str__(self):
		return self.slug

	@property
	def all_benefits(self):
		return self.benefit.all()



class UserMembership(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_membership")
	#stripe_customer_id = models.CharField(max_length=40)
	membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, related_name="membership")

	def __str__(self):
		return self.user.username

def post_save_usermembership_create(sender, instance, created, *args, **kwargs):

	#Creates a userMembership
	if created:
		UserMembership.objects.get_or_create(user=instance)

	#user_membership, created = UserMembership.objects.get_or_create(user=instance)

post_save.connect(post_save_usermembership_create, sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model):
	id = models.AutoField(max_length=7, unique=True, primary_key=True, editable=False)
	user_membership = models.OneToOneField(UserMembership, on_delete=models.CASCADE, related_name="user_membership")
	stripe_subscription_id = models.CharField(max_length=40)
	active = models.BooleanField(default=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="user_subscription")

	def __str__(self):
		return self.user_membership.user.username

	@property
	def get_created_date(self):
		subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
		return datetime.fromtimestamp(subscription.created)

	@property
	def get_next_billing_date(self):
		subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
		return datetime.fromtimestamp(subscription.current_period_end)


class Transaction(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_transaction")
	id = models.AutoField(max_length=7, unique=True, primary_key=True, editable=False)
	subscription = models.OneToOneField(Subscription, on_delete=models.SET_NULL, null=True, related_name="subscription_transaction")
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	tax = models.DecimalField(null=True, max_digits=6, decimal_places=2)
	success = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, editable=True, auto_now=False)

	def __str__(self):
		return '%s (%s)' % (self.user, self.timestamp)

	class Meta:
		ordering = ['-timestamp']
