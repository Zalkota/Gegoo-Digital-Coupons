from django.shortcuts import render

## DEBUG:
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Merchant, Subcategory, Category, FAQ, Context
from django.views.generic import ListView, DetailView, View
# Create your views here.

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from location.functions import set_location_cookies, get_ip, get_or_set_location

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
			#category_nearby_merchants = Merchant.objects.filter(category=category).annotate(distance = Distance("location", user_location)).order_by("distance")[0:9]
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
			merchant = Merchant.objects.get(ref_code=self.kwargs['ref_code'])
			city = 'default_city'
			state = 'default_state'
			city_state = get_or_set_location(self.request)
			city = city_state["city"]
			state = city_state["state"]

			#data = GeoIP.city('google.com')


			context = {
			#'data': data,
            'city': city,
            'state': state,
			'merchant': merchant,
			}
			return render(self.request, "portal/merchant_detail.html", context)

		except ObjectDoesNotExist:
			messages.info(self.request, "Error contact admin")
			return redirect("home-page")


    #def post(self, *args, **kwargs):

    #return redirect("/payment/stripe/")

class FAQView(ListView):
	model = FAQ
	template_name = 'mysite/faq/faq.html'
	# paginate_by = 3

	def get_context_data(self, **kwargs):
		context = super(FAQView, self).get_context_data(**kwargs)
		context['context1'] = Context.objects.get(title='Accounts')
		context['context2'] = Context.objects.get(title='Payment')
		context['context3'] = Context.objects.get(title='Acceptable Offers')
		context['context4'] = Context.objects.get(title='Registration')
		context['context5'] = Context.objects.get(title='User Terms and Conditions')
		return context

class FAQDetailView(DetailView):
	model = FAQ
	template_name = 'mysite/faq/faq-detail.html'

class FAQAccountView(ListView):
	model = FAQ
	template_name = 'mysite/faq/accounts.html'
	queryset = FAQ.objects.filter(context__title = 'Accounts')

	def get_context_data(self, **kwargs):
		context = super(FAQAccountView, self).get_context_data(**kwargs)
		context['context1'] = Context.objects.get(title='Accounts')
		context['context2'] = Context.objects.get(title='Payment')
		context['context3'] = Context.objects.get(title='Acceptable Offers')
		context['context4'] = Context.objects.get(title='Registration')
		context['context5'] = Context.objects.get(title='User Terms and Conditions')
		return context

class FAQPaymentView(ListView):
	model = FAQ
	template_name = 'mysite/faq/payment.html'
	queryset = FAQ.objects.filter(context__title = 'Payment')

	def get_context_data(self, **kwargs):
		context = super(FAQPaymentView, self).get_context_data(**kwargs)
		context['context1'] = Context.objects.get(title='Accounts')
		context['context2'] = Context.objects.get(title='Payment')
		context['context3'] = Context.objects.get(title='Acceptable Offers')
		context['context4'] = Context.objects.get(title='Registration')
		context['context5'] = Context.objects.get(title='User Terms and Conditions')
		return context

class FAQAcceptableOffersView(ListView):
	model = FAQ
	template_name = 'mysite/faq/acceptable-offers.html'
	queryset = FAQ.objects.filter(context__title = 'Acceptable Offers')

	def get_context_data(self, **kwargs):
		context = super(FAQAcceptableOffersView, self).get_context_data(**kwargs)
		context['context1'] = Context.objects.get(title='Accounts')
		context['context2'] = Context.objects.get(title='Payment')
		context['context3'] = Context.objects.get(title='Acceptable Offers')
		context['context4'] = Context.objects.get(title='Registration')
		context['context5'] = Context.objects.get(title='User Terms and Conditions')
		return context