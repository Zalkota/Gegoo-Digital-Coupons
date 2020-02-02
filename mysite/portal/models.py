# <**************************************************************************>
# <*****                         IMPORTS                                *****>
# <**************************************************************************>

from django.db import models
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify

# Image Upload
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator

# Ckeditor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# random_string_generator
import random
import string

# Locations
from cities_light.models import City, Region

# GEODJANGO
from django.contrib.gis.geos import fromstr
from pathlib import Path
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

<<<<<<< HEAD

=======
from users import models as users_models
>>>>>>> subscription

# <**************************************************************************>
# <*****                         CHOICE LISTS                          *****>
# <**************************************************************************>

PAYMENT_OPTION = (
    ('ST', 'Stripe Payment'),
    ('CA', 'Cash Payment'),
    ('OT', 'Other Method')
)

PROMOTION_CHOICES = (
    ('bg-primary', 'primary'),
    ('bg-secondary', 'secondary'),
    ('bg-alt', 'alt')
)

CATEGORY_CHOICES = (
    ('FOOD', 'Food'),
    ('VEHICLES', 'Automotive'),
    ('HOME', 'Home Improvement'),
)

STATUS_CHOICES = {
    ('draft', 'Draft'),
    ('published', 'Published'),
}




ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5

RATING_CHOICES = [
    (ONE, '1 Star'),
    (TWO, '2 Stars'),
    (THREE, '3 Stars'),
    (FOUR, '4 Stars'),
    (FIVE, '5 Stars'),
]

STATUS_CHOCIES = [
    (ONE, 'Being Reviewed'),
    (TWO, 'Published')
]

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

# <**************************************************************************>
# <*****                         MISC FUNCTIONS                         *****>
# <**************************************************************************>

def random_string_generator(size=7, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def random_coupon_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_store_id_generator():
    new_ref_code= random_string_generator()

    qs_exists= store.objects.filter(ref_code=new_ref_code).exists()
    if qs_exists:
        return unique_store_id_generator(instance)
    return new_ref_code

def unique_coupon_generator():
    new_coupon_code = random_coupon_generator()
    return new_coupon_code


# Image Upload Create upload to directory
def upload_to(instance, filename):
    now = timezone.now()
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    return '%s' % (now)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.job.id, filename)


def setStoreRefCode(sender, created, instance, **kwargs):
    store = instance
    #print(store.ref_code)
    if store.ref_code == None:
        try:
            store.ref_code = unique_store_id_generator()
            store.save()
        except:
            print('ERROR REF CODE')


def setCouponCode(sender, created, instance, **kwargs):
    store = instance
    #print(store.ref_code)
    if store.code_coupon == None:
        try:
            coupon_code = str(unique_coupon_generator())
            designation = 'GEGOO'
            code_coupon = designation + coupon_code
            store.code_coupon = code_coupon
            store.save()
        except:
            print('ERROR COUPON CODE')


def CalculateLocation(sender, created, instance, **kwargs):
    store = instance
    #print(store.location)
    if store.location == None:
        try:
            longitude = store.longitude
            latitude = store.latitude

            location = fromstr(
                f'POINT({longitude} {latitude})', srid=4326
            )
            store.location = location
            store.save()

        except KeyError:
            pass

def logo_file_size(value): # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(('File size too large, video must be under 10 MB'))
        
# <**************************************************************************>
# <*****                         MODELS                                 *****>
# <**************************************************************************>


class Images(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='photos/', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])], help_text="Image must be a .PNG or .JPG")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    main_photo = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Images'

    def __str__(self):
        return '%s (%s)' % (self.file, self.uploaded_at)


class Category(models.Model):
    name = models.CharField(choices=CATEGORY_CHOICES, default='FOOD', max_length=20, unique=True, db_index=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portal:category_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=Category)
def pre_save_category(sender, **kwargs):
    slug = slugify(kwargs['instance'].name)
    kwargs['instance'].slug = slug

class Subcategory(models.Model):
    name = models.CharField(max_length=15)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='subcategory')

    class Meta:
        verbose_name_plural = 'Subcategories'

    def __str__(self):
      return '%s' % (self.name)

    def get_absolute_url(self):
        return reverse('portal:subcategory_detail', kwargs={'category': self.category.slug, 'slug': self.slug})

@receiver(pre_save, sender=Subcategory)
def pre_save_subcategory(sender, **kwargs):
    slug = slugify(kwargs['instance'].name)
    kwargs['instance'].slug = slug

class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']


class Offer(models.Model):
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title           = models.CharField(max_length=100, blank=False)
    description     = models.TextField(max_length=500, blank=False)
    # tag             = models.ManyToManyField(Tag, blank=True)
    slug            = models.SlugField(unique=True, blank=True, editable=False)
    end_date        = models.DateField()
    likes           = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    # is_featured     = models.BooleanField('FeaturedStatus', default=False)

    status          = models.PositiveIntegerField(choices=STATUS_CHOCIES, default=1)

    # Creation Fields
    created_at      = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at      = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('users:merchant_offer_detail', kwargs={'slug': self.slug})

    def get_consumer_absolute_url(self):
        return reverse('portal:consumer_offer_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=Offer)
def pre_save_offer(sender, **kwargs):
    slug = slugify(kwargs['instance'].title, kwargs['instance'].id)
    kwargs['instance'].slug = slug


class Store(models.Model):
    active      = models.BooleanField(default=True) #TODO This is not needed, we can just verify
<<<<<<< HEAD
    status      = models.PositiveIntegerField(choices=STATUS_CHOCIES, default=1)
=======
>>>>>>> subscription
    merchant    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # URL Pattern
    slug        = models.SlugField(unique=True, blank=True, null=True) #MAKE THIS NOT EDITABLE

    # Offers
    offers      = models.ManyToManyField(Offer, blank=True)

    # Store Attributes
    business_name       = models.CharField(max_length=100)
    website_url         = models.URLField(max_length=500, blank=True, null=True)
    facebook_url        = models.URLField(max_length=500, blank=True, null=True)
    logo                = models.ImageField(upload_to='store-logos/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), logo_file_size], null=True)


    category            = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    subcategory         = models.ForeignKey(Subcategory, on_delete=models.CASCADE, blank=True, null=True)
    code_coupon         = models.CharField(max_length=15, blank=True, null=True, help_text="If left blank, this will be auto-generated as GEGOO####. Set as 'NONE' if no coupon code is desired for your store.")

    # Store Bio
<<<<<<< HEAD
    title               = models.CharField(max_length=40, null=True, help_text="Company Slogan or catchy short description")
    description         = models.TextField(max_length=500, help_text="Write a summary about your business and its services. Don't list out every service, a short summary will do.")

    # Store Location Info - User fills out
    street_address      = models.CharField(max_length=100, null=True)
    city                = models.CharField(max_length=100, null=True)
    state               = models.CharField(choices=STATES, default='NA', max_length=100)
    zip                 = models.CharField(max_length=100, null=True)
    phone_number        = PhoneNumberField(max_length=20, blank=True, null=True, region='US')

    # Store Location Info - Admin fills out
    latitude            = models.DecimalField(max_digits=11, decimal_places=8, default=1, help_text="Enter latitude of store's location.", null=True, blank=True)
    longitude           = models.DecimalField(max_digits=11, decimal_places=8, default=1, help_text="Enter longitude of store's location.", null=True, blank=True)
    location            = models.PointField(srid=4326, null=True, blank=True, default=None)
=======
    title               = models.CharField(max_length=100)
    description         = models.TextField(max_length=500)

    # Store Location Info
    phone_number        = PhoneNumberField(max_length=20, blank=True, null=True)
    # country             = models.CharField(max_length=40, blank=True) #Not necessary, City covers this.
    # state               = models.CharField(max_length=165, blank=True) #Not necessary, City covers this.
    #city                = models.ForeignKey(City, related_name='store', on_delete=models.CASCADE)
    postal_code         = models.CharField(max_length=12, blank=True)
    latitude            = models.DecimalField(max_digits=11, decimal_places=8, help_text="Enter latitude of store's location.", null=True, blank=True)
    longitude           = models.DecimalField(max_digits=11, decimal_places=8, help_text="Enter longitude of store's location.", null=True, blank=True)
    location            = models.PointField(srid=4326, null=True, blank=True)
>>>>>>> subscription

    # AWS3 Services
    downloadable_content_url            = models.URLField(max_length=500, blank=True, null=True, help_text="Link to AWS download url goes here")
    downloadable_content_title          = models.CharField(max_length=500, blank=True, null=True, help_text="Examples: menu, brochure, etc.")
    promotional_video_file_name         = models.CharField(max_length=1000, blank=True, help_text='Name of the file uploaded to Amazon S3 Bucket. (ie: Video.MP4)')
    promotional_video_thumbnail_name    = models.CharField(max_length=1000, blank=True, help_text='Name of the thumbnail image uploaded to Amazon S3 Bucket (USE .JPG NOT .PNG). (ie: Thumbnail.jpg)')

    ref_code = models.CharField(max_length=20, blank=True, null=True, editable=False)

    #views
    views = models.PositiveIntegerField(default=0) #Does this work? TODO

    # Creation Fields
    created_at      = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at      = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def __str__(self):
        return self.business_name

    def get_absolute_url(self):
        return reverse('portal:merchant_store_detail', kwargs={'slug': self.slug})

    def get_consumer_absolute_url(self):
        return reverse('portal:consumer_store_detail', kwargs={'slug': self.slug})

    @property
    def get_first_active(self):
        now = timezone.now()
        object_qs = self.offers.filter(end_date__gt=now).order_by('end_date')
        object = object_qs.first()
        return object

<<<<<<< HEAD
    @property
    def rating_average(self):
        rating_dict = self.testimonial.all().aggregate(Sum('rating'))
        count = self.testimonial.all().count()
        front_text = rating_dict.get('rating__sum')
        if front_text is not None:
            average_rating = front_text / count
            return average_rating
=======
@receiver(pre_save, sender=Store)
def pre_save_store(sender, **kwargs):
    slug = slugify(kwargs['instance'].business_name)
    kwargs['instance'].slug = slug
    
@receiver([post_save, post_delete], sender=Store)
def update_store_count(sender, instance, **kwargs):
    merchantprofile             = users_models.MerchantProfile.objects.get(user=instance.merchant)
    merchantprofile.stores      = Store.objects.filter(merchant=instance.merchant).count()
    merchantprofile.save()

>>>>>>> subscription

    @property
    def get_total_testimonials(self):
        count = self.testimonial.count()
        return count

<<<<<<< HEAD
    # def GetDistance(self):
    #     return self.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:6]
    #

@receiver(pre_save, sender=Store)
def pre_save_store(sender, **kwargs):
    slug_1 = slugify(kwargs['instance'].business_name, kwargs['instance'].city)
    slug_2 = slugify(slug_1, kwargs['instance'].state)
    slug_3 = slugify(slug_2, kwargs['instance'].id)
    kwargs['instance'].slug = slug_3

post_save.connect(CalculateLocation, sender=Store)
=======
>>>>>>> subscription
post_save.connect(setCouponCode, sender=Store)

class Testimonial(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    store  = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, related_name="testimonial")
    title  = models.CharField(max_length=256, default="")
    review = models.TextField()
    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES, default='5',
        validators = [
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    # Creation Fields
    created_at      = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at      = models.DateTimeField(default=timezone.now, verbose_name="Updated at")




# post_save.connect(setMerchantRefCode, sender=Store)
# post_save.connect(CalculateLocation, sender=Store)

    #
    # def storeCallback(sender, request, user, **kwargs):
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
