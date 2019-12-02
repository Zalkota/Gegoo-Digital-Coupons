from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

#Image Upload
from django.core.validators import FileExtensionValidator

#Ckeditor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

#random_string_generator
import random
import string


PROMOTION_CHOICES = (
    ('bg-primary', 'primary'),
    ('bg-secondary', 'secondary'),
    ('bg-alt', 'alt')
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
    now = timezone_now()
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


class Address(models.Model):

    STATES = (
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

    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, default="")
    state = models.CharField(choices=STATES, default='AL', max_length=100)
    #state = models.ForeignKey('States', on_delete=models.CASCADE, null=True, blank=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    #address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    # default = models.BooleanField(default=False)

    def __str__(self):
        return self.street_address

    class Meta:
        verbose_name_plural = 'Addresses'


class Category(models.Model):
  name = models.CharField(max_length=40, db_index=True, unique=True)

  def __str__(self):
      return self.name


class Subcategory(models.Model):
  name = models.CharField(max_length=40, db_index=True, unique=True)

  def __str__(self):
      return self.name



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
    print(merchant.ref_code)
    if merchant.ref_code == None:
        print('ref_code == None')
        try:
            merchant.ref_code = unique_merchant_id_generator()
            merchant.save()
        except:
            print('ERROR REF CODE')



class Merchant(models.Model):
    business_name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, related_name='address', on_delete=models.SET_NULL, blank=True, null=True)
    logo = models.ImageField(upload_to='merchant-logos/', null=True)
    banner = models.ImageField(upload_to='merchant-banners/', null=True)
    phone_number = PhoneNumberField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='category')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, related_name='subcategory')
    downloadable_content_url =  models.CharField(max_length=500, blank=True, null=True, help_text="Link to AWS download url goes here")
    downloadable_content_title =  models.CharField(max_length=500, blank=True, null=True, help_text="Examples: menu, brochure, etc.")
    website_url = models.CharField(max_length=500)
    facebook_url = models.CharField(max_length=500)
    about = models.ForeignKey(About, related_name='about', on_delete=models.SET_NULL, blank=True, null=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return '%s located in %s, %s.' % (self.business_name, self.address.city, self.address.state)

post_save.connect(setMerchantRefCode, sender=Merchant)

    #
    # def merchantCallback(sender, request, user, **kwargs):
    #     userProfile, is_created = Profile.objects.get_or_create(user=user)
    #     if is_created:
    #         userProfile.name = user.username
    #         userProfile.save()
    #
    # user_signed_up.connect(profileCallback)


class Offer(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, null=True, related_name='merchant')
    title = models.TextField()
    description = RichTextUploadingField()
    # ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True, related_name='ad')
    tag = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField()
    main_image = models.ImageField(upload_to='photos/', null=True)
    end_date = models.DateField()

    def __str__(self):
        return '%s (%s)' % (self.title, self.merchant.name)



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
