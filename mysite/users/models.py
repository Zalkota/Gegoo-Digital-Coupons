from django.contrib.auth.models import AbstractUser
#from django.core.urlresolvers import reverse
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
from location.models import Address
import datetime
from django.utils import timezone


class User(AbstractUser):

<<<<<<< HEAD
    is_merchant     = models.BooleanField('is_merchant', default=False)
    is_approved     = models.BooleanField('merchant_is_approved', default=False)
    has_paid     = models.BooleanField('payment_status', default=False) #Is this necesarry?
    # is_consumer     = models.BooleanField('ConsumerStatus', default=False)
    # slug            = models.SlugField(max_length=100, null=True)

=======
    is_merchant     = models.BooleanField('MerchantStatus', default=False)
    is_approved     = models.BooleanField('ConsumerStatus', default=False)
    slug            = models.SlugField(max_length=100, null=True)
>>>>>>> alpha

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
    # image = models.ImageField(_("Picture"), upload_to=upload_to, null=True, default='blankImage.png', validators=[FileExtensionValidator(['jpg', 'png'])], help_text="Image must be a .PNG or .JPG")
    address = models.OneToOneField(Address, related_name='profile', on_delete=models.CASCADE, blank=True, null=True)
    points = models.PositiveSmallIntegerField(default=0) #Should this be in the user?
    created_time = models.DateTimeField(('created time'), editable=False, null=True, auto_now_add=True)

    def __str__(self):
        return self.user.username


<<<<<<< HEAD
class userStripe(models.Model): #This should only be created for Merchants
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete='CASCADE', related_name='user_stripe')
    stripe_id = models.CharField(max_length=200, null=True, blank=True)
=======
# class userStripe(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete='CASCADE', related_name='user_stripe')
#     stripe_id = models.CharField(max_length=200, null=True, blank=True)
>>>>>>> alpha

#     def __unicode__(self):
#         if self.stripe_id:
#             return str(self.stripe_id)
#         else:
#             return self.user.name

#     def __str__(self):
#         return'%s (%s)' % (self.stripe_id, self.user)

# def stripeCallback(sender, request, user, **kwargs):
#     user_stripe_account, created = userStripe.objects.get_or_create(user=user)
#     if created:
#         print ('test')
#     if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id == '':
#         new_stripe_id = stripe.Customer.create(email=user.email)
#         user_stripe_account.stripe_id = new_stripe_id['id']
#         user_stripe_account.save()


# def addressCallback(sender, request, user, **kwargs):
#     profileAddress, is_created = Address.objects.get_or_create(user=user)
#     print('addressCallBack')
#     if is_created:
#         profileAddress.user = user
#         profileAddress.save()
#         print('addressCallBack', is_created, profileAddress)


# def profileCallback(sender, request, user, **kwargs):
#     userProfile, is_created = Profile.objects.get_or_create(user=user)
#     if is_created:
#         userProfile.name = user.name
#         userProfile.save()
#     try:
#         userAddress = Address.objects.get(user=user)
#         print('user.address', userAddress)
#         userProfile.address = userAddress
#     except:
#         pass

#     userProfile.save()
#     print("profileCallback Created")




# user_logged_in.connect(addressCallback)
# user_logged_in.connect(profileCallback)
# user_logged_in.connect(stripeCallback)

# user_signed_up.connect(addressCallback)
# user_signed_up.connect(profileCallback)
# user_signed_up.connect(stripeCallback)
