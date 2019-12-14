from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Image Upload
from django.core.validators import FileExtensionValidator

# Ckeditor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# random_string_generator
import random
import string

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


class Merchant(models.Model):
    business_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='merchant-logos/', null=True)
    # banner = models.ImageField(upload_to='merchant-banners/', null=True)
    phone_number = PhoneNumberField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='category')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, related_name='subcategory')
    downloadable_content_url =  models.CharField(max_length=500, blank=True, null=True, help_text="Link to AWS download url goes here")
    downloadable_content_title =  models.CharField(max_length=500, blank=True, null=True, help_text="Examples: menu, brochure, etc.")
    website_url = models.CharField(max_length=500)
    facebook_url = models.CharField(max_length=500)
    about = models.ForeignKey(About, related_name='about', on_delete=models.CASCADE, blank=True, null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True, editable=False)
    promotional_video_file_name = models.CharField(max_length=1000, blank=True, help_text='Name of the file uploaded to Amazon S3 Bucket. (ie: Video.MP4)')
    promotional_video_thumbnail_name = models.CharField(max_length=1000, blank=True, help_text='Name of the thumbnail image uploaded to Amazon S3 Bucket (USE .JPG NOT .PNG). (ie: Thumbnail.jpg)')
    #Location
    address = models.ManyToManyField(Address, related_name='merchant')
    latitude = models.DecimalField(max_digits=11, decimal_places=8, help_text="Enter latitude of merchant's location.", null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, help_text="Enter longitude of merchant's location.", null=True, blank=True)
    location = models.PointField(srid=4326, null=True, blank=True)


    def __str__(self):
        return '%s located i' % (self.business_name)

post_save.connect(setMerchantRefCode, sender=Merchant)
post_save.connect(CalculateLocation, sender=Merchant)

    #
    # def merchantCallback(sender, request, user, **kwargs):
    #     userProfile, is_created = Profile.objects.get_or_create(user=user)
    #     if is_created:
    #         userProfile.name = user.username
    #         userProfile.save()
    #
    # user_signed_up.connect(profileCallback)

class OfferManager(models.Manager):
    #Grabs first offer and only shows active offers
    def get_first_active(self):
        now = timezone.now()
        object_qs = Offer.objects.filter(end_date__gt=now).order_by('end_date')
        object = object_qs.first()
        return object


class Offer(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, null=True, related_name='offer')
    address = models.ForeignKey(Address, related_name='offer', on_delete=models.CASCADE, blank=True, null=True)
    title = models.TextField()
    description = RichTextUploadingField()
    # ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True, related_name='ad')
    tag = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField()
    image = models.ImageField(upload_to='photos/', null=True)
    end_date = models.DateField()

    objects = OfferManager()

    def __str__(self):
        return '%s (%s)' % (self.title, self.merchant.business_name)



class Favorite(models.Model):
    offer = models.ForeignKey(Offer, related_name='offer', on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s (%s)' % (self.name, self.offer)




class Promotion(models.Model):
    message = models.CharField(max_length=64)
    background = models.CharField(choices=PROMOTION_CHOICES, default='Primary', max_length=12)
    active = models.BooleanField()
    end_date = models.DateField()

    def __str__(self):
        return '%s' '(%s, ends=%s)' % (self.message, self.active, self.end_date)