from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# Image Upload
from django.core.validators import FileExtensionValidator

# Ckeditor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# random_string_generator
import random
import string

# Locations
from location.models import Address
from cities_light.models import City, Region

# GEODJANGO
from django.contrib.gis.geos import fromstr
from pathlib import Path
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

# Cities


PROMOTION_CHOICES = (
    ('bg-primary', 'primary'),
    ('bg-secondary', 'secondary'),
    ('bg-alt', 'alt')
)

CATEGORY_CHOICES = (
    ('FOOD', 'Food & Dining'),
    ('VEHICLES', 'Automotive & Transportation'),
)


def random_string_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_merchant_id_generator():
    new_ref_code= random_string_generator()

    qs_exists= Merchant.objects.filter(ref_code=new_ref_code).exists()
    if qs_exists:
        return unique_merchant_id_generator(instance)
    return new_ref_code



# Image Upload Create upload to directory
def upload_to(instance, filename):
    now = timezone.now()
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    return '%s' % (now)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.job.id, filename)

class Images(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='photos/', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])], help_text="Image must be a .PNG or .JPG")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    main_photo = models.BooleanField()

    def __str__(self):
        return '%s (%s)' % (self.file, self.uploaded_at)

class Category(models.Model):
    name = models.CharField(choices=CATEGORY_CHOICES, default='FOOD', max_length=20, unique=True, db_index=True,)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portal:category_detail', kwargs={'name': self.name})

class Subcategory(models.Model):
  name = models.CharField(max_length=40, db_index=True, unique=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='subcategory')

  def __str__(self):
      return '%s' % (self.name)

class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']

class About(models.Model):
    header = models.TextField()
    subheader = models.TextField()
    body = RichTextUploadingField()
    # services_header = models.CharField(max_length=100)
    images = models.ManyToManyField(Images, blank=True, help_text="Alternate Photos of Product")
    #services = models.TextField()

    def __str__(self):
        return '%s' % (self.header)

def setMerchantRefCode(sender, created, instance, **kwargs):
    merchant = instance
    #print(merchant.ref_code)
    if merchant.ref_code == None:
        print('ref_code == None')
        try:
            merchant.ref_code = unique_merchant_id_generator()
            merchant.save()
        except:
            print('ERROR REF CODE')

def CalculateLocation(sender, created, instance, **kwargs):
    merchant = instance
    #print(merchant.location)
    if merchant.location == None:
        try:
            longitude = merchant.longitude
            latitude = merchant.latitude

            location = fromstr(
                f'POINT({longitude} {latitude})', srid=4326
            )
            merchant.location = location
            merchant.save()

        except KeyError:
            pass

class Offer(models.Model):
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title           = models.CharField(max_length=100, blank=False)
    description     = models.TextField(max_length=500, blank=False)
    tag             = models.ManyToManyField(Tag, blank=True)
    slug            = models.SlugField(unique=True)
    image           = models.ImageField(upload_to='photos/', null=True)
    end_date        = models.DateField()
    likes           = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    # is_featured     = models.BooleanField('FeaturedStatus', default=False)

    # Creation Fields
    created_at      = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at      = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portal:merchant_offer_detail', kwargs={'slug': self.slug})
    
    def get_consumer_absolute_url(self):
        return reverse('portal:consumer_offer_detail', kwargs={'slug': self.slug})
    
@receiver(pre_save, sender=Offer)
def pre_save_offer(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug

class Store(models.Model):
    merchant    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # URL Pattern
    slug        = models.SlugField(unique=True)

    # Offers
    offers      = models.ManyToManyField(Offer)

    # Store Attributes
    business_name       = models.CharField(max_length=100)
    website_url         = models.URLField(max_length=500, blank=True, null=True)
    facebook_url        = models.URLField(max_length=500, blank=True, null=True)
    logo                = models.ImageField(upload_to='merchant-logos/', blank=True, null=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category')


    # Store Bio
    title               = models.CharField(max_length=100)
    description         = models.TextField(max_length=500)

    # Store Location Info
    phone_number        = PhoneNumberField(max_length=20, blank=True, null=True)
    country             = models.CharField(max_length=40, blank=True)
    state               = models.CharField(max_length=165, blank=True)
    city                = models.ManyToManyField(City, related_name='merchant', blank=True)
    postal_code         = models.CharField(max_length=12, blank=True)
    latitude            = models.DecimalField(max_digits=11, decimal_places=8, help_text="Enter latitude of merchant's location.", null=True, blank=True)
    longitude           = models.DecimalField(max_digits=11, decimal_places=8, help_text="Enter longitude of merchant's location.", null=True, blank=True)
    location            = models.PointField(srid=4326, null=True, blank=True)

    # AWS3 Services
    downloadable_content_url            = models.URLField(max_length=500, blank=True, null=True, help_text="Link to AWS download url goes here")
    downloadable_content_title          = models.CharField(max_length=500, blank=True, null=True, help_text="Examples: menu, brochure, etc.")
    promotional_video_file_name         = models.CharField(max_length=1000, blank=True, help_text='Name of the file uploaded to Amazon S3 Bucket. (ie: Video.MP4)')
    promotional_video_thumbnail_name    = models.CharField(max_length=1000, blank=True, help_text='Name of the thumbnail image uploaded to Amazon S3 Bucket (USE .JPG NOT .PNG). (ie: Thumbnail.jpg)')

    ref_code = models.CharField(max_length=20, blank=True, null=True, editable=False)

    # Creation Fields
    created_at      = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at      = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def __str__(self):
        return self.business_name

    def get_absolute_url(self):
        return reverse('portal:merchant_store_detail', kwargs={'slug': self.slug})

    def get_consumer_absolute_url(self):
        return reverse('portal:consumer_store_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=Store)
def pre_save_store(sender, **kwargs):
    slug = slugify(kwargs['instance'].business_name)
    kwargs['instance'].slug = slug

# post_save.connect(setMerchantRefCode, sender=Store)
# post_save.connect(CalculateLocation, sender=Store)

    #
    # def merchantCallback(sender, request, user, **kwargs):
    #     userProfile, is_created = Profile.objects.get_or_create(user=user)
    #     if is_created:
    #         userProfile.name = user.username
    #         userProfile.save()
    #
    # user_signed_up.connect(profileCallback)
#
# class OfferManager(models.Manager):
#     #Grabs first offer and only shows active offers
#     def get_first_active(self):
#         now = timezone.now()
#         object_qs = Offer.objects.filter(end_date__gt=now).order_by('end_date')
#         object = object_qs.first()
#         return object

class Promotion(models.Model):
    message = models.CharField(max_length=64)
    background = models.CharField(choices=PROMOTION_CHOICES, default='Primary', max_length=12)
    active = models.BooleanField()
    end_date = models.DateField()

    def __str__(self):
        return '%s' '(%s, ends=%s)' % (self.message, self.active, self.end_date)
