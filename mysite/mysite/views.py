from django.shortcuts import render
from django.db.models import Subquery
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View
import datetime
from django.utils import timezone
# Contact Form
from django.views.generic.edit import FormView, FormMixin

from django.http import HttpResponse
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone

# imports
from location.models import Address
from .models import Contact
from portal.models import Offer, Store, Category, Address

#mail
from django.core.mail import send_mail
from django.template.loader import render_to_string

#messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

#Customer email import
from django.conf import settings
EMAIL_CUSTOMER = settings.EMAIL_CUSTOMER


#GeoIP
from geolite2 import geolite2
import json

from location.functions import set_location_cookies, get_ip, get_or_set_location


#TODO Remove me
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from django.db.models import Q, Max
import operator

def get_items(request):
    items_qs = Item.objects.all()
    if items_qs.exists():
        return items_qs
    return None





# def post_comment(request):
#     if request.method != 'POST':
#         raise Http404('Only POSTs are allowed')
#
#     if 'comment' not in request.POST:
#         raise Http404('Comment not submitted')
#
#     if request.session.get('has_commented', False):
#         return HttpResponse("You've already commented.")
#
#     c = comments.Comment(comment=request.POST['comment'])
#     c.save()
#     request.session['has_commented'] = True
#     return HttpResponse('Thanks for your comment!')


#
# data {
# 'city':
#     {'geoname_id': 5004062, 'names':
#         {'en': 'Novi', 'ja': 'ノバイ', 'ru': 'Новый'}
#     },
# 'continent':
#     {'code': 'NA', 'geoname_id': 6255149, 'names':
#         {'de': 'Nordamerika', 'en': 'North America', 'es': 'Norteamérica', 'fr': 'Amérique du Nord', 'ja': '北アメリカ', 'pt-BR': 'América do Norte', 'ru': 'Северная Америка', 'zh-CN': '北美洲'}
#     },
# 'country':
#     {'geoname_id': 6252001, 'iso_code': 'US', 'names':
#         {'de': 'USA', 'en': 'United States', 'es': 'Estados Unidos', 'fr': 'États-Unis', 'ja': 'アメリカ合衆国', 'pt-BR': 'Estados Unidos', 'ru': 'США', 'zh-CN': '美国'}
#     },
# 'location':
#     {'accuracy_radius': 200, 'latitude': 42.4634, 'longitude': -83.4646, 'metro_code': 505, 'time_zone': 'America/Detroit'},
# 'postal':
#     {'code': '48375'},
# 'registered_country':
#     {'geoname_id': 6252001, 'iso_code': 'US', 'names':
#         {'de': 'USA', 'en': 'United States', 'es': 'Estados Unidos', 'fr': 'États-Unis', 'ja': 'アメリカ合衆国', 'pt-BR': 'Estados Unidos', 'ru': 'США', 'zh-CN': '美国'}
#     },
# 'subdivisions': [
#     {'geoname_id': 5001836, 'iso_code': 'MI', 'names':
#         {'en': 'Michigan', 'es': 'Michigan', 'fr': 'Michigan', 'ja': 'ミシガン州', 'pt-BR': 'Michigão', 'ru': 'Мичиган', 'zh-CN': '密歇根州'}
#     }]
# }
#
#
# class SetLocationMixin(object):
#     model = None
#
#     def main(self):
#         if "state" in request.GET:
#
#             # Create an HttpResponse object...
#             response = HttpResponse("Your state is %s" % \
#                 request.GET["state"])
#
#             # ... and set a cookie on the response
#             response.set_cookie("state",
#                                 request.GET["state"])
#
#             return response
#
#         else:
#
#         return HttpResponse("No state found")



# # Find what country the .ly TLD belongs to
# >>> Country.objects.get(tld='ly')
# <Country: Libya>
#
# # 5 Nearest cities to London
# >>> london = City.objects.filter(country__name='United Kingdom').get(name='London')
# >>> nearest = City.objects.distance(london.location).exclude(id=london.id).order_by('distance')[:5]
#
# # All cities in a state or county
# >>> City.objects.filter(country__code="US", region__code="TX")
# >>> City.objects.filter(country__name="United States", subregion__name="Orange County")



class homeView(View):

    def get(self, *args, **kwargs):
<<<<<<< HEAD

        city = 'default_city'
        state = 'default_state'
        city_state = get_or_set_location(self.request)
        city = city_state["city"]
        state = city_state["state"]
        address_qs = Merchant.objects.filter(city__name=city)
        merchant_empty_qs = Merchant.objects.all()[0:6]
        category_list = Category.objects.all()
        # city = context["city"]
        # state = context["subdivisions"]
        #merchant_nearby = Merchant.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:6]
        #merchant_nearby = Merchant.objects.annotate(distance = Distance("location", user_location)).annotate(offer_title=Subquery(Offer.values('end_date')[:1])).order_by("distance")

        # if address_qs = None:
        #     address_qs = Address.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:6]
        city = 'default_city'
        state = 'default_state'
        city_state = get_or_set_location(self.request)

        city = city_state["city"]
        state = city_state["state"]

        print(city)
        # city = context["city"]
        # state = context["subdivisions"]
        #Store_nearby = Store.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:6]
        #Store_nearby = Store.objects.annotate(distance = Distance("location", user_location)).annotate(offer_title=Subquery(Offer.values('end_date')[:1])).order_by("distance")
        address_qs = Store.objects.filter(city=city)
        # if address_qs = None:
        #     address_qs = Address.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:6]
        category_list = Category.objects.all()
>>>>>>> alpha
=======
>>>>>>> alpha


        # reader = geolite2.reader()
        # data = reader.get('107.77.193.143')
        # print('data', data)
        #
        # print('city', data["city"]['names']['en'])

        context = {
            'city': city,
            'state': state,
            'address_qs': address_qs,
            'merchant_empty_qs': merchant_empty_qs,
            'category_list': category_list,
        }
        return render(self.request, 'mysite/home_page.html', context)



def security(request):
    return render(request, 'security.txt')

def components(request):

    return render(request, 'components/main.html')
