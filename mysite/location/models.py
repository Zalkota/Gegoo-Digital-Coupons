# Create your models here.
from __future__ import unicode_literals
from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.conf import settings
from cities_light.models import City, Region

# customization
from cities_light.abstract_models import (AbstractCity, AbstractRegion,
AbstractCountry)
from cities_light.receivers import connect_default_signals

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True, related_name='address')
    street_address = models.CharField(max_length=100, blank=True, null=True)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    zip = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return '%s' % (self.city)

    class Meta:
        verbose_name_plural = 'Addresses'
