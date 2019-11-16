from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from allauth.account.signals import user_logged_in, user_signed_up
#payments
import stripe
#Image Upload
from django.core.validators import FileExtensionValidator

#Ckeditor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


# Image Upload Create upload to directory
def upload_to(instance, filename):
    now = timezone_now()
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    return '%s' % (now)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.job.id, filename)

RETURN_CHOICES = (
    ('F', 'Found a better deal'),
    ('S', 'Not satisfied with the quality'),
    ('T', 'Took too long to arrive'),
    ('N', 'None of the above')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

ORDER_CHOICES = (
    ('A', 'ATTENTION NEEDED'),
    ('P', 'PROCESSING'),
    ('D', 'DELIVERED'),
    ('S', 'SHIPPED'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def stripeCallback(sender, request, user, **kwargs):
    user_stripe_account, created = UserProfile.objects.get_or_create(user=user)
    if created:
        print ('test')
    if user_stripe_account.stripe_customer_id is None or user_stripe_account.stripe_customer_id == '':
        new_stripe_id = stripe.Customer.create(email=user.email)
        user_stripe_account.stripe_customer_id = new_stripe_id['id']
        user_stripe_account.save()

user_logged_in.connect(stripeCallback)
user_signed_up.connect(stripeCallback)


class Category(models.Model):
  name = models.CharField(max_length=255, db_index=True, unique=True)

  def __str__(self):
      return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']


class Image(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='photos/', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])], help_text="Image must be a .PNG or .JPG")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    main_photo = models.BooleanField()

#    class Meta:
#        ordering = ['-main_photo']

    def __str__(self):
        return '%s (%s)' % (self.file, self.uploaded_at)



class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='category')
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    tag = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField()
    description = RichTextUploadingField()
    main_image = models.ImageField(upload_to='photos/', null=True)
    images = models.ManyToManyField(Image, blank=True, help_text="Alternate Photos of Product")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shoppingcart:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("shoppingcart:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("shoppingcart:remove-from-cart", kwargs={
            'slug': self.slug
        })





class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return  '(%s) %s' % (self.quantity, self.item.title)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    arrival_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    status = models.CharField(choices=ORDER_CHOICES, max_length=1, default="P")
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    class Meta:
        ordering = ['-ordered_date']

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


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

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default="")
    state = models.CharField(choices=STATES, default='AL', max_length=100)
    #state = models.ForeignKey('States', on_delete=models.CASCADE, null=True, blank=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class States(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=96)
    state_abbr = models.CharField(max_length=24, blank=True)


    #Define the __unicode__ method, which is used by related models by default.
    def __unicode__(self):
        return self.state_abbr

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.CharField(choices=LABEL_CHOICES, max_length=1)
    message = models.TextField(null=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.pk)



def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
