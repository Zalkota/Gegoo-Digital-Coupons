from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.urls import reverse
import uuid
import json
from django.utils.encoding import python_2_unicode_compatible

#Rating System
from django.db.models import Sum

#from users.models import Profile
import users.models
from memberships.models import Membership

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

class Appointment(BaseModel):
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
    TYPE_CHOICES = (
        (One, ''),
        (Two, ''),
        (Three, ''),
        (Four, ''),
        (Five, ''),
        (Six, ''),
        (SEVEN, ''),
        (EIGHT, ''),
        (NINE, ''),
        (TEN, ''),
        (ELEVEN, ''),
        (TWELVE, ''),
    )
    first_name = models.CharField(max_length=50, help_text="First name")
    last_name = models.CharField(max_length=50, help_text="Last name")
    company = models.CharField(max_length=50, help_text="Company")
    email = models.CharField(max_length=50, help_text="Email")
    appointment_time = models.PositiveSmallIntegerField(('Pick a time to schedule a over the phone consultation'), choices=TYPE_CHOICES, default=None, db_index=True)


class Course(models.Model):
    slug = models.SlugField()
    ordering_id = models.PositiveIntegerField(null=True, help_text='Ordering of courses to be displayed [Atleast one course must start at one]')
    title = models.CharField(max_length=60)
    card_description = models.TextField(max_length=60, default="No Description")
    description = models.TextField(max_length=255)
    image_url = models.CharField(max_length=500, help_text="AWS image url. Dimensions: 600x400 Format: .JPG", null=True)
    subject = models.CharField(max_length=30, help_text="Math, Science, English, etc.", default="Math")
    targeted_grades = models.CharField(max_length=45, help_text="3rd, 4th, 5th, etc.", default="3rd Grade")
    course_content_1 = models.CharField(max_length=75, help_text="Write a small paragraph about what this course offers", default="Please Add a Description")
    course_content_2 = models.CharField(max_length=75, help_text="Write a small paragraph about what this course offers", default="Please Add a Description")
    course_content_3 = models.CharField(max_length=75, help_text="Write a small paragraph about what this course offers", default="Please Add a Description")
    course_content_4 = models.CharField(max_length=75, help_text="Write a small paragraph about what this course offers", default="Please Add a Description")
    course_content_5 = models.CharField(max_length=75, help_text="Write a small paragraph about what this course offers", default="Please Add a Description")
    course_content_6 = models.CharField(max_length=75, help_text="Write a small paragraph about what this course offers", default="Please Add a Description")
    allowed_memberships = models.ManyToManyField(Membership)
    membership_required = models.BooleanField(default=True, help_text=('Does this course require a membership'), db_index=True)
    tags = models.CharField(max_length=100, default="course", help_text="Write keywords that describe this course, this helps the websites search engine. Lower case words and include title of course.")


    def __str__(self):
        return '%s (%s)' % (self.title, self.ordering_id)

    def get_absolute_url(self):
        return reverse('portal:course_detail', kwargs={'slug': self.slug})
    @property
    def all_memberships(self):
        return self.allowed_memberships.all()

    @property
    def lessons(self):
        return self.lesson.all().order_by('ordering_id')

    @property
    def first_lesson(self):
        lesson_qs = self.lesson.all().order_by('ordering_id')
        first_lesson = lesson_qs.first()
        return first_lesson.slug

    @property
    def rating_average(self):
        rating_dict = self.course_review.all().aggregate(Sum('rating'))
        count = self.course_review.all().count()
        front_text = rating_dict.get('rating__sum')
        if front_text is not None:
            average_rating = front_text / count
            return average_rating



class Lesson(models.Model):
    ordering_id = models.PositiveIntegerField(null=True, help_text="This represents the ordering of each individual lesson, if this is the first lesson of the course it should be 1.",)
    slug = models.SlugField(    help_text="Use 'lesson-#' # will equal the number you put in position. Such as 1,2,3,etc.",)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=25, help_text="Enter a name for this Course",)
    description = models.CharField(max_length=40, help_text="Enter a short description", default="Please add a lesson description")
    detailed_description = models.CharField(max_length=500, help_text="Enter a long description explaining this course to the customer", default="Please add a lesson description")

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, help_text="This lesson is part of which course?", null=True, related_name="lesson")
    document = models.FileField(null=True, blank=True, help_text="Upload PDF")
    powerpoint_link = models.CharField(max_length=200, help_text="AWS Excel Download Link", null=True, blank=True)
    video_url = models.CharField(max_length=200, help_text="AWS Video Link",)
    video_thumbnail = models.CharField(max_length=200, help_text="Upload a .JPG", null=True)

    def __str__(self):
        return self.title

    @property
    def first_lesson(self):
        lesson_qs = self.lesson.all().order_by('ordering_id')
        first_lesson = lesson_qs.first()
        return first_lesson.slug

    def get_absolute_url(self):
        return reverse('portal:lesson_detail',
        kwargs={
        'course_slug': self.course.slug,
        'lesson_slug': self.slug
        })

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
    review_course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1, related_name="course_review")
    summary = models.CharField(max_length=255, help_text=('what did you think about this course?'))
    rating = models.PositiveSmallIntegerField(('Rate this course between 1-5 stars.'), choices=TYPE_CHOICES, default=Five, db_index=True)
    created_time = models.DateTimeField(('created time'), editable=False, auto_now_add=True)



    def __str__(self):
        return '%s (%s)' % (self.review_user, self.rating)
