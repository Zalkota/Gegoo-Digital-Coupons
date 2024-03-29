from django.contrib.auth.models import AbstractUser
#from django.core.urlresolvers import reverse
from location.models import City
from django.shortcuts import reverse
import os
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now
from django.conf import settings
from allauth.account.signals import user_logged_in, user_signed_up
import stripe
from django.core.validators import FileExtensionValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import datetime
from django.utils import timezone


# GEODJANGO
from django.contrib.gis.geos import fromstr
from pathlib import Path
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from portal import models as portal_models

#Stripe import key
STRIPE_PUB_KEY = settings.STRIPE_PUB_KEY
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY

STATUS_CHOICES = (
    ('INITIAL', 'Initial'),
    ('PENDING', 'Pending Approval'),
    ('APPROVED', 'Approved'),
    ('DENIED', 'Denied'),
)

STATES = (
        ("NA", "-"),
        ("AL", "Alabama"),
        ("AK", "Alaska"),
        ("AS", "American Samoa"),
        ("AZ", "Arizona"),
        ("AR", "Arkansas"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("DC", "District Of Columbia"),
        ("FM", "Federated States Of Micronesia"),  #TODO: WHAT THE FUCK IS THIS?!?!?
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("GU", "Guam"),
        ("HI", "Hawaii"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("IA", "Iowa"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("ME", "Maine"),
        ("MH", "Marshall Islands"),
        ("MD", "Maryland"),
        ("MA", "Massachusetts"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MS", "Mississippi"),
        ("MO", "Missouri"),
        ("MT", "Montana"),
        ("NE", "Nebraska"),
        ("NV", "Nevada"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NY", "New York"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("MP", "Northern Mariana Islands"),  #TODO: FIXME: http://thepythondjango.com/list-usa-states-python-django-format/
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PW", "Palau"),
        ("PA", "Pennsylvania"),
        ("PR", "Puerto Rico"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VT", "Vermont"),
        ("VI", "Virgin Islands"),
        ("VA", "Virginia"),
        ("WA", "Washington"),
        ("WV", "West Virginia"),
        ("WI", "Wisconsin"),
        ("WY", "Wyoming")
        )

class User(AbstractUser):
    is_merchant         = models.BooleanField('is_merchant', default=False)
    city                = models.ForeignKey(City, related_name='user_city', default='1', on_delete=models.CASCADE, null=True, blank=True)


    # User Location
    location            = models.PointField(srid=4326, null=True, blank=True)

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
    points = models.PositiveSmallIntegerField(default=0) #Should this be in the user?

    def __str__(self):
        return self.user.username


#TODO Only created for non-merchants
def ProfileCallback(sender, request, user, **kwargs):
    if user.is_merchant == False:
        userProfile, is_created = Profile.objects.get_or_create(user=user)


class MerchantProfile(models.Model): #Is a Profile Necessary?
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='merchant_profile')
    customer_id     = models.CharField(max_length=200, null=True, blank=True)
    status          = models.CharField(choices=STATUS_CHOICES, default='INITIAL', max_length=20)
    content_uploaded    = models.BooleanField('Has this user uploaded content?', default=False)

    payment_status  = models.BooleanField(default=False)


    #Address
    street_address  = models.CharField(max_length=100, blank=True, null=True)
    city            = models.CharField(max_length=100, blank=True, null=True)
    state           = models.CharField(choices=STATES, default='NA', max_length=100)
    zip             = models.CharField(max_length=100, blank=True, null=True)
    phone_number    = PhoneNumberField(max_length=20, blank=True, null=True)

    # Store Info
    stores = models.PositiveIntegerField(default=0, validators = [MinValueValidator(0)])

    #Online links
    website_url         = models.CharField(max_length=500, blank=True, null=True)
    facebook_url         = models.CharField(max_length=500, blank=True, null=True)

    #Misc
    created_at      = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at      = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def get_absolute_url(self):
        return reverse('merchant_profile_update', kwargs={'pk': self.pk})


    def __str__(self):
        return self.user.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_merchant_profile(sender, instance, created, **kwargs):
    if instance.is_merchant==True:
        if created:
            MerchantProfile.objects.get_or_create(user=instance)

        merchantprofile, created = MerchantProfile.objects.get_or_create(user=instance)

        if merchantprofile.customer_id is None or merchantprofile.customer_id == '':
            stripe.api_key                   = STRIPE_SECRET_KEY
            stripe_customer_id               = stripe.Customer.create(email=instance.email, name='%s %s' % (instance.first_name, instance.last_name))
            merchantprofile.customer_id      = stripe_customer_id['id']
            merchantprofile.save()

@receiver(post_save, sender=MerchantProfile)
def create_stripe_customer_id(sender, instance, **kwargs):
    merchant_profile                     = MerchantProfile.objects.get(user=instance.user)

    if merchant_profile.customer_id is None or merchant_profile.customer_id == '':
        stripe.api_key                   = STRIPE_SECRET_KEY
        stripe_customer_id               = stripe.Customer.create(email=instance.user.email, name='%s %s' % (instance.user.first_name, instance.user.last_name))
        merchant_profile.customer_id     = stripe_customer_id['id']
        merchant_profile.save()

class Follow(models.Model):
    connections         = models.ManyToManyField(settings.AUTH_USER_MODEL)
    current_user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner', null=True)

    @classmethod
    def add_connection(cls, current_user, new_connection):
        follow, created = cls.objects.get_or_create(
            current_user = current_user
        )
        follow.connections.add(new_connection)

    @classmethod
    def remove_connection(cls, current_user, new_connection):
        follow, created = cls.objects.get_or_create(
            current_user = current_user
        )
        follow.connections.remove(new_connection)

# user_logged_in.connect(addressCallback)
# user_logged_in.connect(profileCallback)
# user_logged_in.connect(stripeCallback)

user_signed_up.connect(ProfileCallback)
# post_save.connect(create_merchant_profile, sender=User)
# user_signed_up.connect(stripeCallback)
