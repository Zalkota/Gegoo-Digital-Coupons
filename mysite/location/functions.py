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

def set_location_cookies(request, city, state):
    response = HttpResponse("setting state to %s, city to %s" % (state, city))
    response.set_cookie('ct', city)
    response.set_cookie('st', state)
    print (state, city)
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
    data = reader.get('107.77.193.143')
    return data


def get_or_set_location(request):
    if request.user.is_authenticated:
        #Check if user has address
        if request.user.user_profile.address.city and request.user.user_profile.address.state != None:
            city = request.user.user_profile.address.city
            state = request.user.user_profile.address.state

            context = {
            'city': city,
            'state': state,
            }
            return context
        # If it doesnt lets add one from IP address
        else:
            try:
                data = get_ip(request)
                #Obtain City and State from IP address
                city = data["city"]['names']['en']
                state = data["subdivisions"][0]['iso_code']
                print (city, ', ', state)
                # Save data to user address
                user_address = request.user.user_profile.address
                user_address.state = state
                user_address.city = city
                # user_address.user =
                user_address.save()

                context = {
                'city': city,
                'state': state,
                }
                return context
            except:
                pass

    elif not request.user.is_authenticated:
        #Check cookies for city and state
        if 'st' and 'ct' in request.COOKIES:
            state = request.COOKIES['st']
            city = request.COOKIES['ct']
            print('location found in cookies')

            context = {
            'city': city,
            'state': state,
            }
            return context
        # Else lets use their IP address to find out and then add it to their Cookies
        else:
            print('attemtping to obtain IP address location')
            data = get_ip(request)
            #Obtain City and State from IP address
            city = data["city"]['names']['en']
            state = data["subdivisions"][0]['iso_code']
            #Add City and State to Cookies for next time
            set_location_cookies(request, city, state)
            context = {
            'city': city,
            'state': state,
            }
            return context
