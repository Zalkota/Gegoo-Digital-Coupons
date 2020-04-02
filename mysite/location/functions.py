#GeoIP
from geolite2 import geolite2
import json
from django.shortcuts import render
from django.db.models import Subquery
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.http import HttpResponse
from allauth.account.signals import user_logged_in, user_signed_up
from cities_light.models import Region, City
from django.conf import settings

# GEODJANGO
from django.contrib.gis.geos import fromstr
from pathlib import Path
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


def set_location_cookies(request, city, state):
    response = HttpResponse("setting state to %s, city to %s" % (state, city))
    response.set_cookie('ct', city)
    response.set_cookie('st', state)
    # print (state, city)
    return response


# Obtain the Users IP Address
def get_ip(request):
    x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forward != None:
        ip = x_forward.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    #We should have IP address at this point
    reader = geolite2.reader()
    data = reader.get(ip)

    if data == None:
        data = reader.get('107.77.193.143')
    return data


def get_or_set_location(request):
    user = request.user
    if request.user.is_authenticated:
        #Check if user has address

        try:
            if request.user.city and user.location != None:
                city = request.user.city
                location = request.user.location
                # print('1')

                context = {
                'city': city.name,
                'state': city.region.name,
                'user_location': location,
                }
                return context

            else:
                data = get_ip(request)
                #Obtain City and State from IP address
                city = data["city"]['names']['en']
                state = data["subdivisions"][0]['names']['en']
                # Query object so that we can save it into the database
                city_qs = City.objects.get(name=city, region__name=state)

                # Use City to set spacial database location
                location_data = CalculateCityLocation(request, city_qs)

                # Save data to user address
                user = request.user
                user.city = city_qs
                user.location = location_data
                user.save()

                context = {
                'city': city_qs.name,
                'state': city_qs.region.name,
                'user_location': location_data,
                }
                return context
        except:
            pass

    if not request.user.is_authenticated:
        #Check cookies for city and state
        if 'st' and 'ct' in request.COOKIES:
            state = request.COOKIES['st']
            city = request.COOKIES['ct']
            location = request.COOKIES['loc']

            context = {
            'city': city,
            'state': state,
            'user_location': location,
            }
            return context
        # Else lets use their IP address to find out and then add it to their Cookies
        else:
            # print('attemtping to obtain IP address location')
            data = get_ip(request)
            #Obtain City and State from IP address
            city = data["city"]['names']['en']
            state = data["subdivisions"][0]['names']['en']

            city_qs = City.objects.get(name=city, region__name=state)

            location_data = CalculateCityLocation(request, city_qs)
            #Add City and State to Cookies for next time
            set_location_cookies(request, city, state)
            context = {
            'city': city,
            'state': state,
            'user_location': location_data
            }
            return context



def CalculateCityLocation(request, city):
    try:
        longitude = city.longitude
        latitude = city.latitude

        # print('long,lat', longitude, latitude)

        location = fromstr(
            f'POINT({longitude} {latitude})', srid=4326
        )
        return location

    except KeyError:
        pass


#
# def setAddressCallback(sender, request, user, **kwargs):
#     user_address, is_created = Address.objects.get_or_create(user=user)
#
#     print('Lets try to get ip from database')
#     #Check if user has address
#     if user_address.city and user_address.state != None:
#         city = user_address.city
#         state = user_address.state
#
#         context = {
#         'city': city,
#         'state': state,
#         }
#         return context
#     # If it doesnt lets add one from IP address
#     else:
#         print('Lets try to get ip from geo database')
#         data = get_ip(request)
#         #Obtain City and State from IP address
#         city = data["city"]['names']['en']
#         state = data["subdivisions"][0]['names']['en']
#         print (city, ', ', state)
#
#         city_qs = City.objects.get(name=city)
#         state_qs = Region.objects.get(name=state)
#
#         # Save data to user address
#         user_address.state = state_qs
#         user_address.city = city_qs
#         user_address.save()
#
#         context = {
#         'city': city,
#         'state': state,
#         }
#
#
# user_logged_in.connect(setAddressCallback)
