from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from . import views
from portal import models as portal_models
from support import models as support_models


## Tutorial https://www.youtube.com/watch?v=xAXMqiPSY34

class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home-page', 'security']

    def location(self, item):
        return reverse(item)

class SupportSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['support:questions_list', 'support:contact-page', 'support:about-page', 'support:contact-landing-page']

    def location(self, item):
        return reverse(item)

class QuestionSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return support_models.Question.objects.all()

    def location(self, item):
        return reverse(item)

class TopicSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return support_models.Topic.objects.all()

    def location(self, item):
        return reverse(item)

class StoreSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return portal_models.Store.objects.filter(status=2)

class CategorySitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return portal_models.Category.objects.all()

class SubcategorySitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return portal_models.Subcategory.objects.all()
