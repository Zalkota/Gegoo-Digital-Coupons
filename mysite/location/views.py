from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from cities_light.models import City, Region

# latitude = 42.637740
# longitude = -83.363546
#
#
# user_location = Point(longitude, latitude, srid=4326)
#
#
# class Home(generic.ListView):
#     model = Shop
#     context_object_name = "shops"
#
#     queryset = Shop.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:6]
#
#     template_name = "shops/index.html"
#
#
def SearchAddress(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
        if search_text == '':
            address = None
        else:
            address = City.objects.filter(name__contains=search_text)
    return render(request,'location/ajax_search.html', {'address' : address })
