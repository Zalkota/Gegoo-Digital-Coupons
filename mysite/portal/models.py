from django.db import models
from datetime import date, timezone
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.urls import reverse
import uuid
import json
from django.utils.encoding import python_2_unicode_compatible
from django.template.defaultfilters import slugify

#Rating System
from django.db.models import Sum

#from users.models import Profile
import users.models

from django.core.validators import FileExtensionValidator
#from user_profile.models import User
#from users.models import Profile
#from django.apps import apps
#User1 = apps.get_model('users', 'User')


@python_2_unicode_compatible
class BaseModel(models.Model):
    #TODO: Add queryset managers / mixins
    is_active = models.BooleanField(default=True, help_text=('Designates whether this item should be treated as active. Unselect this instead of deleting data.'), db_index=True) #TODO: Can I hide this on the model form unless user has permissions or do I do this in forms.py? Change these to 'visible' or 'is_active'??
    created_time = models.DateTimeField(('created time'), editable=False, auto_now_add=True)
    modified_time = models.DateTimeField(('last modified time'), editable=False, auto_now=True)


    #  id = models.BigAutoField(primary_key=True)
    class Meta:
        abstract = True

# Image Upload Create upload to directory
def upload_to(instance, filename):
    now = timezone_now()
    base, ext = os.path.splitext(filename)
    ext = ext.lower()
    return '%s' % (now)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.job.id, filename)




class Job(BaseModel):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    TYPE_CHOICES = (
    (One, '24 Hours'),
    (Two, '3 Days'),
    (Three, '7 Days'),
    )

    STATUS_CHOICES = (
    ("IN PROGRESS", 'In Progress'),
    ("REQUIRES INPUT", 'Requires Input'),
    ("COMPLETED", 'Completed'),
    ("AWAITING PAYMENT", 'Awaiting Payment')
    )

    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=2500, help_text="Please describe the details of your project to our design team (500-2500 characters)", verbose_name="Job Description")
    desired_plants = models.TextField(max_length=500, blank=True, null=True, help_text="What types of plants, trees, and shrubs will be required?", verbose_name="Plants, Trees, and Shrubs")
    hardscaping = models.BooleanField(verbose_name="Will there be Hardscaping for this project?", default=False)
    hardscaping_description = models.TextField(max_length=500, help_text="If yes, please describe the required hardscaping required", verbose_name="If yes, Please describe in detail", blank=True, null=True)
    due_date = models.PositiveSmallIntegerField(('Once you place your order, when would you like your service delivered?'), choices=TYPE_CHOICES, default=Two, db_index=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='AWAITING PAYMENT', db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, related_name="user_job")
    designer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, related_name="designer_job")
    #image = models.ImageField(("Picture"), upload_to=upload_to, null=True, default='blankImage.png', validators=[FileExtensionValidator(['jpg', 'png'])], help_text="Image must be a .PNG or .JPG")


    def __str__(self):
        return '%s (%s)' % (self.user, self.created_time)

    def get_absolute_url(self):
        return reverse('portal:job_detail', kwargs={'slug': self.slug})





class Image(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='photos/', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])], help_text="Image must be a .PNG or .JPG")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_image", null=True)

    def __str__(self):
        return '%s (%s)' % (self.file, self.uploaded_at)

class Review(models.Model):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    TYPE_CHOICES = (
        (One, '1 Star'),
        (Two, '2 Stars'),
        (Three, '3 Stars'),
        (Four, '4 Stars'),
        (Five, '5 Stars'),
    )
    review_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, related_name="user_review")
    review_job = models.ForeignKey(Job, on_delete=models.CASCADE, default=1, related_name="job_review")
    summary = models.CharField(max_length=255, help_text=('what did you think about thisjob?'))
    rating = models.PositiveSmallIntegerField(('Rate this job between 1-5 stars.'), choices=TYPE_CHOICES, default=Five, db_index=True)
    created_time = models.DateTimeField(('created time'), editable=False, auto_now_add=True)

    def __str__(self):
        return '%s (%s)' % (self.review_user, self.rating)


class Transaction(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_transaction")
	order_id = models.CharField(max_length=36, unique=True, default=uuid.uuid4, primary_key=True, editable=False)
	job = models.ForeignKey(Job, blank=True, on_delete=models.CASCADE, null=True, related_name="job_transaction")
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	success = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, editable=True, auto_now=False)

	def __str__(self):
		return '%s (%s)' % (self.order_id, self.user)

	class Meta:
		ordering = ['-timestamp']
