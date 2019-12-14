# Create your models here.
from __future__ import unicode_literals
from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from cities_light.models import City, Region
#
# latitude = 42.637740
# longitude = -83.363546
#
#
# user_location = Point(longitude, latitude, srid=4326)
#
# class Shop(models.Model):
#     name = models.CharField(max_length=100)
#     location = models.PointField(srid=4326)
#     address = models.CharField(max_length=100)
#     city = models.CharField(max_length=50)
#
#     # def GetDistance(self):
#     #     trim = True
#     #     return Shop.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:6]
#
#     def __unicode__(self):
#         return self.name


class Address(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100, blank=True, null=True)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    # state = models.ForeignKey(Country, default='NA', blank=True, null=True, max_length=30)
    state = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    # country = CountryField(multiple=False, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    #address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    # default = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.city)

    class Meta:
        verbose_name_plural = 'Addresses'
