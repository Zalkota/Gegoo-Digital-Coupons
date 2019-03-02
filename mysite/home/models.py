from django.db import models
from project.models import ProjectPage, ProjectIndexPage
from portal.models import Course
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

#Captcha
from wagtailcaptcha.models import WagtailCaptchaEmailForm

# forms http://docs.wagtail.io/en/v2.0/reference/contrib/forms/
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel, PageChooserPanel
)
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from django.shortcuts import redirect



class HomePage(Page):
    firstheader = models.CharField(blank=True, max_length=100)
    firstbody = models.CharField(blank=True, max_length=100)
    registerbuttonurl = models.CharField(blank=True, max_length=250)
    secondheader = RichTextField(blank=True)
    secondbody = RichTextField(blank=True)

    def special_projects(self):
        return ProjectPage.objects.all()

    def course_list(self):
        return Course.objects.filter(membership_required=True).order_by('ordering_id')[:4]

    content_panels = Page.content_panels + [

        FieldPanel('firstheader', classname="full"),
        FieldPanel('firstbody', classname="full"),
        FieldPanel('registerbuttonurl'),
        InlinePanel('gallery_images', label="Gallery images"),
        FieldPanel('secondheader', classname="full"),
        FieldPanel('secondbody', classname="full"),
    ]

class HomePageGalleryImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class PrivacyPage(Page):
    header = RichTextField(blank=True)
    content = RichTextField(blank=True)
    content_panels = Page.content_panels + [
    FieldPanel('header', classname="full"),
    FieldPanel('content', classname="full"),
    ]

class TermsPage(Page):
    header = RichTextField(blank=True)
    content = RichTextField(blank=True)
    content_panels = Page.content_panels + [
    FieldPanel('header', classname="full"),
    FieldPanel('content', classname="full"),
    ]

class AboutPage(Page):
    header = RichTextField(blank=True)
    body = RichTextField(blank=True)
    header_two = RichTextField(blank=True)
    body_two = RichTextField(blank=True)
    header_three = RichTextField(blank=True)
    body_three = RichTextField(blank=True)
    header_four = RichTextField(blank=True)
    body_four = RichTextField(blank=True)
    header_five = RichTextField(blank=True)
    body_five = RichTextField(blank=True)
    video_url = models.CharField(blank=True, max_length=250)
    video_thumbnail = models.CharField(blank=True, max_length=250, help_text="Upload a JPG",  null=True)

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        FieldPanel('body', classname="full"),
        FieldPanel('header_two'),
        FieldPanel('body_two', classname="full"),
        FieldPanel('header_three'),
        FieldPanel('body_three', classname="full"),
        FieldPanel('header_four'),
        FieldPanel('body_four', classname="full"),
        FieldPanel('header_five'),
        FieldPanel('body_five', classname="full"),
        FieldPanel('video_url'),
        FieldPanel('video_thumbnail'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

class AboutPageGalleryImage(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(WagtailCaptchaEmailForm):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    address = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('body', classname='full'),
        FieldPanel('address', classname='full'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


    thank_you_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    def render_landing_page(self, request, form_submission=None, *args, **kwargs):
        if self.thank_you_page:
            url = self.thank_you_page.url
            # if a form_submission instance is available, append the id to URL
            # when previewing landing page, there will not be a form_submission instance
            if form_submission:
              url += '?id=%s' % form_submission.id
            return redirect(url, permanent=False)
        # if no thank_you_page is set, render default landing page
        return super().render_landing_page(request, form_submission, *args, **kwargs)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname='full'),
        FieldPanel('body', classname='full'),
        FieldPanel('address', classname='full'),
        InlinePanel('form_fields'),
        FieldPanel('thank_you_text', classname='full'),
        PageChooserPanel('thank_you_page'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col6'),
                FieldPanel('to_address', classname='col6'),
            ]),
            FieldPanel('subject'),
        ], 'Email'),
    ]



class JobField(AbstractFormField):
    page = ParentalKey('JobPage', on_delete=models.CASCADE, related_name='form_fields')


class JobPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]


    thank_you_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    def render_landing_page(self, request, form_submission=None, *args, **kwargs):
        if self.thank_you_page:
            url = self.thank_you_page.url
            # if a form_submission instance is available, append the id to URL
            # when previewing landing page, there will not be a form_submission instance
            if form_submission:
              url += '?id=%s' % form_submission.id
            return redirect(url, permanent=False)
        # if no thank_you_page is set, render default landing page
        return super().render_landing_page(request, form_submission, *args, **kwargs)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro', classname='full'),
        InlinePanel('form_fields'),
        FieldPanel('thank_you_text', classname='full'),
        PageChooserPanel('thank_you_page'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col6'),
                FieldPanel('to_address', classname='col6'),
            ]),
            FieldPanel('subject'),
        ], 'Email'),
    ]
