from django.db import models
from datetime import date
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
#get_absolute_url
from django.urls import reverse
from django.utils.text import slugify
#Ckeditor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


@python_2_unicode_compatible
class BaseModel(models.Model):
    #TODO: Add queryset managers / mixins
    is_active = models.BooleanField(default=True, help_text=('Designates whether this item should be treated as active. Unselect this instead of deleting data.'), db_index=True) #TODO: Can I hide this on the model form unless user has permissions or do I do this in forms.py? Change these to 'visible' or 'is_active'??
    created_time = models.DateTimeField(('created time'), editable=False, auto_now_add=True, blank=True, null=True)
    modified_time = models.DateTimeField(('last modified time'), editable=False, auto_now=True)
    #  id = models.BigAutoField(primary_key=True)
    class Meta:
        abstract = True

class Reservation(BaseModel):
    class Meta:
        verbose_name_plural = "Reservations"
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    TIME_CHOICES = (
        (One, '4:00pm'),
        (Two, '4:30pm'),
        (Three, '5:00pm'),
        (Four, '5:30pm'),
        (Five, '6:00pm'),
        (Six, '6:30pm'),
        (SEVEN, '7:00pm'),
        (EIGHT, '7:30pm'),
        (NINE, '8:00pm'),
    )
    SEATING_CHOICES = (
        (One, '1'),
        (Two, '2'),
        (Three, '3'),
        (Four, '4'),
        (Five, '5'),
        (Six, '6'),
        (SEVEN, '7'),
        (EIGHT, '8'),
        (NINE, '9'),
        (TEN, '10+'),
    )
    date = models.DateField(null=True)
    name = models.CharField(max_length=35, null=True)
    phone = PhoneNumberField(null=True)   #USE THIS https://github.com/stefanfoulis/django-phonenumber-field
    email = models.EmailField(null=True)
    people = models.PositiveSmallIntegerField(choices=SEATING_CHOICES, default=None, db_index=True)
    reservation_time = models.PositiveSmallIntegerField(choices=TIME_CHOICES, default=None, db_index=True)

    def __str__(self):
        return '(%s) %s %s' % (self.date, self.name, self.phone )


class Page(BaseModel):
    slug = models.SlugField(null=True, unique=True, editable=False)
    title = models.CharField(max_length=200, help_text='TITLE MUST BE UNIQUE')
    main_header = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    header_1 = RichTextUploadingField(null=True, blank=True)
    body_1 = RichTextUploadingField(null=True, blank=True)
    section = models.CharField(max_length=10000, null=True, blank=True)
    header_2 = RichTextUploadingField(null=True, blank=True)
    body_2 = RichTextUploadingField(null=True, blank=True)
    created_date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(BaseModel):
    slug = models.SlugField(null=True, unique=True, editable=False)
    name = models.CharField(max_length=200, help_text='Name must be unique')
    image = models.ImageField(upload_to = 'product_images/', help_text="All Images must be 800x600px")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class Furnace(BaseModel):
    slug = models.SlugField(null=True, unique=True, editable=False)
    name = models.CharField(max_length=200, help_text='Name must be unique')
    description = RichTextUploadingField(null=True, blank=True)
    productNumber = models.CharField(max_length=200, null=True)
    price = models.PositiveSmallIntegerField(default = timezone.now)
    image = models.ImageField(upload_to = 'product_images/', help_text="All Images must be 800x600px")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class AirConditioning(BaseModel):
    slug = models.SlugField(null=True, unique=True, editable=False)
    name = models.CharField(max_length=200, help_text='Name must be unique')
    description = RichTextUploadingField(null=True, blank=True)
    productNumber = models.CharField(max_length=200, null=True)
    price = models.PositiveSmallIntegerField(default = timezone.now)
    image = models.ImageField(upload_to = 'product_images/', help_text="All Images must be 800x600px")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class Service(BaseModel):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to = 'product_images/', help_text="All Images must be 800x600px")

    def __str__(self):
        return '%s' % (self.name)

class Review(BaseModel):
    description = models.CharField(max_length=256)
    customer = models.CharField(max_length=256, help_text="Customer first and last name")
    city = models.CharField(max_length=256)

    def __str__(self):
        return '%s' % (self.customer)

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = PhoneNumberField(null=True, blank=True)   #USE THIS https://github.com/stefanfoulis/django-phonenumber-field\
    description = models.TextField()


    #def get_absolute_url(self):
    #    return reverse('author-detail', kwargs={'pk': self.pk})

class Coupon(BaseModel):
    name = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to = 'product_images/', help_text="All Images must be 800x600px")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
