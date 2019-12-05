from django.views import generic
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Shop

latitude = 42.637740
longitude = -83.363546


user_location = Point(longitude, latitude, srid=4326)

def truncate(n, decimals=2):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

class Home(generic.ListView):
    model = Shop
    context_object_name = "shops"

    trim = True
    #
    # distanceFunction = (Distance("location", user_location))/meterMileConversion
    #
    # truncatedDistance = truncate(distanceFunction)

    def truncate(n):
        multiplier = 10 ** 2
        return int(n * multiplier) / multiplier

    queryset = Shop.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:6]

    template_name = "shops/index.html"
