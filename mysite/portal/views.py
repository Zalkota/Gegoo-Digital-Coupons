from django.shortcuts import render

## DEBUG:
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Merchant, Subcategory, Category
from django.views.generic import ListView, DetailView, View
# Create your views here.

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
latitude = 42.637740
longitude = -83.363546
user_location = Point(longitude, latitude, srid=4326)


def get_user_orders(request, user):
	user_orders_qs = Order.objects.filter(user=user)
	if user_orders_qs.exists():
		return user_orders_qs
	return None

class CategoryListView(ListView):
	model = Category


class CategoryDetailView(View):

	def get(self, *args, **kwargs):
		try:
			category = Category.objects.get(name=self.kwargs['name'])
			category_nearby_merchants = Merchant.objects.filter(category=category).annotate(distance = Distance("location", user_location)).order_by("distance")[0:9]
			all_categories = Category.objects.all()

			context = {
			'category': category,
			'category_nearby_merchants': category_nearby_merchants,
			'all_categories': all_categories,
			}
			return render(self.request, "portal/category_detail.html", context)

		except ObjectDoesNotExist:
			messages.info(self.request, "Error contact admin")
			return redirect("home-page")


# class SubcategoryListView(View):
# 	def get(self, *args, **kwargs):
# 		try:
# 			merchant = Subcategory.objects.filter(category=self.kwargs['category'])


class MerchantDetailView(View):
	def get(self, *args, **kwargs):
		try:
			merchant = Merchant.objects.get(id=self.kwargs['id'])
			recommended_offers = Merchant.objects.annotate(distance = Distance("location", user_location)).order_by("distance")[0:4]

			#data = GeoIP.city('google.com')


			context = {
			#'data': data,
			'merchant': merchant,
			'recommended_offers': recommended_offers,
			}
			return render(self.request, "portal/merchant_detail.html", context)

		except ObjectDoesNotExist:
			messages.info(self.request, "Error contact admin")
			return redirect("home-page")


    #def post(self, *args, **kwargs):

    #return redirect("/payment/stripe/")
