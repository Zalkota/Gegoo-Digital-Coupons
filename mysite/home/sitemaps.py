from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from home.models import Page
from . import views



## Tutorial https://www.youtube.com/watch?v=xAXMqiPSY34

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home-page', 'contact-page', 'contact-landing-page']

    def location(self, item):
        return reverse(item)


class PageSitemap(Sitemap):

    def items(self):
        return Page.objects.all()
