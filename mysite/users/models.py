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
from portal.models import Address
import datetime
from django.utils import timezone

MERCHANT_SELECT = (
    ("NO", "No"),
    ("YES", "Yes")
    )

class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name_of_User'), blank=True, max_length=255)
    merchant_select = models.CharField(choices=MERCHANT_SELECT, default='NO', max_length=2)
    #accepted_terms_of_service = models.Booleanfield()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

# Profile Image
def upload_to(instance, filename):
    now = timezone_now()
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    return '%s' % (now)

    #return "profile/{{now:%Y/%m/%Y%m%d%H%M%S}{ext}"



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    # image = models.ImageField(_("Picture"), upload_to=upload_to, null=True, default='blankImage.png', validators=[FileExtensionValidator(['jpg', 'png'])], help_text="Image must be a .PNG or .JPG")
    created_time = models.DateTimeField(('created time'), editable=False, null=True, auto_now_add=True)
    address = models.OneToOneField(Address, related_name='profile', on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.CharField(max_length=120, default='ABC')

    def __str__(self):
        return self.user.username


class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete='CASCADE', related_name='user_stripe')
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        if self.stripe_id:
            return str(self.stripe_id)
        else:
            return self.user.username

    def __str__(self):
        return'%s (%s)' % (self.stripe_id, self.user)

def stripeCallback(sender, request, user, **kwargs):
    user_stripe_account, created = userStripe.objects.get_or_create(user=user)
    if created:
        print ('test')
    if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id == '':
        new_stripe_id = stripe.Customer.create(email=user.email)
        user_stripe_account.stripe_id = new_stripe_id['id']
        user_stripe_account.save()


def profileCallback(sender, request, user, **kwargs):
    userProfile, is_created = Profile.objects.get_or_create(user=user)
    if is_created:
        userProfile.name = user.username
        userProfile.save()

user_logged_in.connect(stripeCallback)
user_signed_up.connect(profileCallback)
user_signed_up.connect(stripeCallback)
