from django.contrib.auth.models import AbstractUser
#from django.core.urlresolvers import reverse
from location.models import City

import os
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now
from django.conf import settings
from allauth.account.signals import user_logged_in, user_signed_up
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.core.validators import FileExtensionValidator

import datetime
from django.utils import timezone


class User(AbstractUser):
    is_merchant     = models.BooleanField('is_merchant', default=False)
    is_approved     = models.BooleanField('merchant_is_approved', default=False)
    has_paid     = models.BooleanField('payment_status', default=False) #Is this necesarry?
    # is_consumer     = models.BooleanField('ConsumerStatus', default=False)
    # slug            = models.SlugField(max_length=100, null=True)

    created_at      = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at      = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def __str__(self):
        return self.username
    #
    # def get_absolute_url(self):
    #     return reverse('users:detail', kwargs={'username': self.name})
    #     return reverse('users:detail', kwargs={'user': self.username})

# Profile Image
def upload_to(instance, filename):
    now = timezone_now()
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    return '%s' % (now)

    #return "profile/{{now:%Y/%m/%Y%m%d%H%M%S}{ext}"


class Profile(models.Model): #Is a Profile Necessary?
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    city = models.ForeignKey(City, related_name='profile', on_delete=models.CASCADE, null=True, blank=True)
    points = models.PositiveSmallIntegerField(default=0) #Should this be in the user?

    def __str__(self):
        return self.user.username



class userStripe(models.Model): #This should only be created for Merchants
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete='CASCADE', related_name='user_stripe')
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        if self.stripe_id:
            return str(self.stripe_id)
        else:
            return self.user.name

    def __str__(self):
        return'%s (%s)' % (self.stripe_id, self.user)


# TODO Only created for merchants
def stripeCallback(sender, request, user, **kwargs):
    if user.is_merchant == True:
        user_stripe_account, created = userStripe.objects.get_or_create(user=user)
        try:
            if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id == '':
                new_stripe_id = stripe.Customer.create(email=user.email)
                user_stripe_account.stripe_id = new_stripe_id['id']
                user_stripe_account.save()
                print("stripeCallback Created")
        except:
            pass


#TODO Only created for non-merchants
def profileCallback(sender, request, user, **kwargs):
    if user.is_merchant == False:
        userProfile, is_created = Profile.objects.get_or_create(user=user)
        print("profileCallback Created")


# user_logged_in.connect(addressCallback)
# user_logged_in.connect(profileCallback)
# user_logged_in.connect(stripeCallback)

user_signed_up.connect(profileCallback)
user_signed_up.connect(stripeCallback)
