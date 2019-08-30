from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
import uuid
from datetime import datetime
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class Discount(models.Model):
	name = models.CharField(max_length=80)
	percentage = models.DecimalField(max_digits=6, decimal_places=2)

	def get_percentage(self):
		return self.percentage * 100
		total = property(get_percentage)

	def __str__(self):
		return '%s (%s)' % (self.name, self.percentage)

class Charge(models.Model):
	description = models.CharField(max_length=80)
	hours = models.DecimalField(max_digits=6, decimal_places=2)
	rate = models.DecimalField(max_digits=6, decimal_places=2)

	def get_total(self):
		return self.hours * self.rate
		total = property(get_total)

	def __str__(self):
		return '%s' % (self.description)

class Invoice(models.Model):

	slug = models.SlugField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoice")
	invoice_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4, primary_key=True, editable=False)
	payed = models.BooleanField(default=False, help_text="Has the customer payed?")
	description = models.CharField(max_length=255, default="add description")
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	tax = models.DecimalField(null=True, max_digits=6, decimal_places=2)
	issue_date = models.DateField(auto_now_add=True, auto_now=False, null=True)
	due_date = models.DateField(auto_now_add=False, auto_now=False, null=True)
	discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name="discount_invoice", null=True, blank=True)
	charge = models.ManyToManyField(Charge)

	def __str__(self):
		return self.description

	class Meta:
		ordering = ('-issue_date', 'due_date')
		verbose_name = "Invoice"
		verbose_name_plural = "Invoices"

	#def get_total(self):
    #    return sum([item.product.price for item in self.tax])

	# Factories

    # Mutators

    # Queries

    # Properties

	@property
	def get_total(self):
		return self.tax + self.amount
		total = property(get_total)

	@property
	def stripe_total(self):
		calculate = (self.tax + self.amount) * 100
		result = int(calculate)
		print ('amount=', result)
		return result
		total = property(stripe_total)

	@property
	def all_charges(self):
		return self.charge.all()





class Benefit(models.Model):
	name = models.CharField(max_length=36)

	def __str__(self):
		return self.name

class Membership(models.Model):
	MEMBERSHIP_CHOICES = (
	('Website Hosting', 'Website Hosting'),
	('PPC Advertising', 'PPC Advertising'),
	('Digital Marketing', 'Digital Marketing')
	)
	slug = models.SlugField()
	position = models.PositiveSmallIntegerField(null=True)
	membership_type = models.CharField(
			choices=MEMBERSHIP_CHOICES,
			default='Website Hosting',
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
		return self.membership_type

	@property
	def all_benefits(self):
		return self.benefit.all()


class UserMembership(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_membership")
	#stripe_customer_id = models.CharField(max_length=40)
	membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True, related_name="membership")

	def __str__(self):
		return self.user.username

def post_save_usermembership_create(sender, instance, created, *args, **kwargs):

	#Creates a userMembership
	if created:
		UserMembership.objects.get_or_create(user=instance)

	user_membership, created = UserMembership.objects.get_or_create(user=instance)


post_save.connect(post_save_usermembership_create, sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model):
	id = models.CharField(max_length=36, unique=True, default=uuid.uuid4, primary_key=True, editable=False)
	user_membership = models.OneToOneField(UserMembership, on_delete=models.CASCADE)
	stripe_subscription_id = models.CharField(max_length=40)
	active = models.BooleanField(default=True)

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
	order_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4, primary_key=True, editable=False)
	subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name="subscription_transaction")
	invoice_id = models.CharField(max_length=36, null=True, blank=True)
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	tax = models.DecimalField(null=True, max_digits=6, decimal_places=2)
	success = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, editable=True, auto_now=False)

	def __str__(self):
		return '%s (%s)' % (self.order_id, self.user)

	class Meta:
		ordering = ['-timestamp']
