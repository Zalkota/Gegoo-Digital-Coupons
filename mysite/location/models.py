# Create your models here.
from __future__ import unicode_literals
from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


latitude = 42.637740
longitude = -83.363546


user_location = Point(longitude, latitude, srid=4326)

class Shop(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField(srid=4326)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    # def GetDistance(self):
    #     trim = True
    #     return Shop.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:6]

    def __unicode__(self):
        return self.name
