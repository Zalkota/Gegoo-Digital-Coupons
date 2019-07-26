from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index

class ProjectIndexPage(Page):
    header = RichTextField(blank=True)
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('intro', classname="full"),
        FieldPanel('body', classname="full")
    ]


class ProjectPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    image_url_thumbnail = models.CharField(blank=True, max_length=250, help_text="Image link")
    title_1 = RichTextField(blank=True)
    body_1 = RichTextField(blank=True)
    image_url_1 = models.CharField(blank=True, max_length=250, help_text="Image link")
    title_2 = RichTextField(blank=True)
    body_2 = RichTextField(blank=True)
    image_url_2 = models.CharField(blank=True, max_length=250, help_text="Image link")
    title_3 = RichTextField(blank=True)
    body_3 = RichTextField(blank=True)
    image_url_3 = models.CharField(blank=True, max_length=250, help_text="Image link")
    work_done = models.CharField(max_length=250, default="UI / UX Design • Web Development")
    location = models.CharField(max_length=40, default="Flint, MI")
    website_url = models.CharField(blank=True, max_length=250)
    active = models.BooleanField(default=False)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body_1'),
        index.SearchField('location'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('work_done'),
        FieldPanel('location'),
        FieldPanel('website_url'),
        FieldPanel('image_url_thumbnail'),
        FieldPanel('image_url_1'),
        FieldPanel('image_url_2'),
        FieldPanel('image_url_3'),
        FieldPanel('intro'),
        FieldPanel('title_1', classname="full"),
        FieldPanel('body_1', classname="full"),
        FieldPanel('title_2', classname="full"),
        FieldPanel('body_2', classname="full"),
        FieldPanel('title_3', classname="full"),
        FieldPanel('body_3', classname="full"),
        FieldPanel('active'),
    ]
