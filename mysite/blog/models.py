from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index

class Tag(models.Model):
	name = models.CharField(max_length=36)

	def __str__(self):
		return self.name


class BlogIndexPage(Page):


    content_panels = Page.content_panels + [

    ]

class BlogPage(Page):
    TYPE_CHOICES = (
    ("Technology", 'TECHNOLOGY'),
    ("Marketing", 'MARKETING'),
    )
    date = models.DateField("Post date")
    category = models.CharField(max_length=12, choices=TYPE_CHOICES, default=None, null=True, blank=True, db_index=True)
    header = models.CharField(max_length=75)
    body = RichTextField(blank=True)
    description = RichTextField(blank=True)
    author = models.CharField(max_length=75)
    tag = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to = 'blog_images/', null=True, help_text="All Images must be 800x600px")
    active = models.BooleanField(default=False)

    search_fields = Page.search_fields + [
        index.SearchField('header'),
        index.SearchField('body'),
        index.SearchField('author'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('category'),
        FieldPanel('header'),
        FieldPanel('body', classname="full"),
        FieldPanel('description', classname="full"),
        FieldPanel('author'),
        FieldPanel('tag'),
        FieldPanel('image'),
        FieldPanel('active'),
    ]

    @property
    def all_tag(self):
        return self.tag.all()
