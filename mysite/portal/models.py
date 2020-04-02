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

from users import models as users_models

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
    ('ALL', 'All Services'),
    ('AUTO', 'Auto'),
    ('BEAUTY', 'Beauty'),
    ('COMMUNITY', 'Community'),
    ('CONSTRUCTION', 'Construction'),
    ('FOOD', 'Food'),
    ('FUN', 'Fun'),
    ('GARDEN', 'Garden'),
    ('GROCERIES', 'Groceries'),
    ('HEALTH', 'Health'),
    ('HOME', 'Home Improvement'),
    ('PETS', 'Pets'),
    ('RETAIL', 'Retail'),
)

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

STATUS_CHOICES = [
    (ONE, 'Draft'),
    (THREE, 'Pending'),
    (TWO, 'Published'),
    (FOUR, 'Denied'),
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


# def setStoreRefCode(sender, created, instance, **kwargs):
#     store = instance
#     #print(store.ref_code)
#     if store.ref_code == None:
#         try:
#             store.ref_code = unique_store_id_generator()
#             store.save()
#         except:
#             print('ERROR REF CODE')


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
    slug = models.SlugField(unique=True, blank=True, editable=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portal:category_detail', kwargs={'slug': self.slug})

@receiver(pre_save, sender=Category)
def pre_save_category(sender, **kwargs):
    slug = slugify(kwargs['instance'].name.capitalize())
    print(slug.capitalize())
    kwargs['instance'].slug = slug

class Subcategory(models.Model):
    name = models.CharField(max_length=25)
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
    slug = slugify(kwargs['instance'].name.capitalize())
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
    slug            = models.SlugField(unique=True, blank=True, editable=False)
    end_date        = models.DateField()
    likes           = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')

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

class StoreVideoManager(models.Manager):
    #Grabs first offer and only shows active offers
    def get_nearby_videos(self):
        stores_qs = Store.objects.filter(end_date__gt=now).order_by('end_date')
        object = object_qs.first()
        return object

class Store(models.Model):
    subscription_status     = models.BooleanField(default=False) #TODO This is not needed, we can just verify
    status                  = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1)
    merchant                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # URL Pattern
    slug                = models.SlugField(unique=True, blank=True, null=True) #MAKE THIS NOT EDITABLE

    # Store Attributes
    business_name       = models.CharField(max_length=100)
    website_url         = models.URLField(max_length=500, blank=True, null=True)
    facebook_url        = models.URLField(max_length=500, blank=True, null=True)
    logo                = models.ImageField(upload_to='store-logos/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], null=True)


    category            = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    subcategory         = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)
    code_coupon         = models.CharField(max_length=15, blank=True, null=True, help_text="If left blank, this will be auto-generated as GEGOO####. Set as 'NONE' if no coupon code is desired for your store.")

    # Store Bio
    slogan               = models.CharField(max_length=40, null=True, help_text="Slogan or catchy short description")
    description         = models.TextField(help_text="Describe the store", null=True)

    # Store Location Info - User fills out
    street_address      = models.CharField(max_length=100, blank=True, null=True)
    city                = models.CharField(max_length=100, null=True)
    state               = models.CharField(choices=STATES, default='NA', max_length=100)
    zip                 = models.CharField(max_length=100, blank=True, null=True)
    phone_number        = PhoneNumberField(max_length=20, blank=True, null=True, region='US', help_text="Example: 123 456-7890")

    # Store Location Info - Admin fills out
    latitude            = models.DecimalField(max_digits=11, decimal_places=8, default=1, help_text="Enter latitude of store's location.", null=True, blank=True)
    longitude           = models.DecimalField(max_digits=11, decimal_places=8, default=1, help_text="Enter longitude of store's location.", null=True, blank=True)
    location            = models.PointField(srid=4326, null=True, blank=True, default=None)

    ref_code = models.CharField(max_length=20, blank=True, null=True, editable=False)

    #views
    views = models.PositiveIntegerField(default=0) #Does this work? TODO

    # Creation Fields
    created_at      = models.DateTimeField(default=timezone.now, verbose_name="Created at")
    updated_at      = models.DateTimeField(default=timezone.now, verbose_name="Updated at")

    def __str__(self):
        return self.business_name

    def get_absolute_url(self):
        return reverse('users:merchant_store_detail', kwargs={'slug': self.slug})

    def get_consumer_absolute_url(self):
        return reverse('portal:consumer_store_detail', kwargs={'slug': self.slug})


    #TODO
    # https://docs.djangoproject.com/en/3.0/ref/models/options/#indexes
    # class Meta:
    #     indexes = [
    #         models.Index(fields=['location']), #Is this enough? Most queries only look for location.
    #         models.Index(fields=['location', 'business_name']),
    #     ]


    @property
    def rating_average(self):
        rating_dict = self.testimonial.all().aggregate(Sum('rating'))
        count = self.testimonial.all().count()
        front_text = rating_dict.get('rating__sum')
        if front_text is not None:
            average_rating = front_text / count
            return average_rating

    @property
    def rating_average_round(self):
        rating_dict = self.testimonial.all().aggregate(Sum('rating'))
        count = self.testimonial.all().count()
        front_text = rating_dict.get('rating__sum')
        if front_text is not None:
            average_rating = front_text / count
            average_rating_rounded = round(average_rating)
            return range(average_rating_rounded)

    @property
    def rating_average_round_inverted(self):
        rating_dict = self.testimonial.all().aggregate(Sum('rating'))
        count = self.testimonial.all().count()
        front_text = rating_dict.get('rating__sum')
        if front_text is not None:
            average_rating = front_text / count
            average_rating_rounded = round(average_rating)
            return range(5-average_rating_rounded)

    @property
    def get_total_testimonials(self):
        count = self.testimonial.count()
        return count

@receiver([post_save, post_delete], sender=Store)
def update_store_count(sender, instance, **kwargs):
    merchant_profile_qs = users_models.MerchantProfile.objects.filter(user=instance.merchant)

    if merchant_profile_qs.exists():
        merchantprofile             = merchant_profile_qs.first()

        #Update store count
        merchantprofile.stores      = Store.objects.filter(merchant=instance.merchant).count()

        #Update User Status if store is approved
        if instance.status          == 2:
            merchantprofile.status  = 'APPROVED'

        #Save changes
        merchantprofile.save()
    else:
        pass

post_save.connect(CalculateLocation, sender=Store)
post_save.connect(setCouponCode, sender=Store)


class TestimonialManager(models.Manager):
    #Grabs first offer and only shows active offers
    def testimonials_capped(self):
        object_list = self.order_by('-created_at')[:5]
        return object_list

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
    created_at      = models.DateField(default=timezone.now, verbose_name="Created at")
    updated_at      = models.DateField(default=timezone.now, verbose_name="Updated at")

    objects = TestimonialManager()

    # @property
    # def four(self):
    #     return self.order_by('-created_at')[:5]

    @property
    def range(self):
        rating_range = range(self.rating)
        return rating_range

    @property
    def range_inverted(self):
        rating_range = range( 5-self.rating)
        return rating_range

class StoreOffer(models.Model):
    offers = models.ManyToManyField(Offer)
    current_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='storeoffer', null=True)

    @classmethod
    def add_offer(cls, current_store, new_offer):
        storeoffer, created = cls.objects.get_or_create(
            current_store = current_store
        )
        storeoffer.offers.add(new_offer)

    @classmethod
    def remove_offer(cls, current_store, new_offer):
        storeoffer, created = cls.objects.get_or_create(
            current_store = current_store
        )
        storeoffer.offers.remove(new_offer)

class FollowStore(models.Model):
    connections         = models.ManyToManyField(Store)
    current_user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user', null=True)

    def __str__(self):
        return '%s %s - Store Favorite List' % (self.current_user.first_name, self.current_user.last_name)

    @classmethod
    def add_connection(cls, current_user, new_connection):
        follow_store, created = cls.objects.get_or_create(
            current_user = current_user
        )
        follow_store.connections.add(new_connection)

    @classmethod
    def remove_connection(cls, current_user, new_connection):
        follow_store, created = cls.objects.get_or_create(
            current_user = current_user
        )
        follow_store.connections.remove(new_connection)
