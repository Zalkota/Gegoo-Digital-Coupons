# <**************************************************************************>
# <*****                         IMPORTS                                *****>
# <**************************************************************************>
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.text import slugify
from django.conf import settings
## DEBUG:
#messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from portal import models as portal_models
from django.views.generic import ListView, DetailView, View, CreateView, DeleteView, UpdateView
# Create your views here.

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from location.functions import set_location_cookies, get_ip, get_or_set_location
from users.decorators import user_is_merchant
from .forms import MerchantStoreForm, MerchantTestimonialForm
from users.decorators import IsMerchantMixin, IsUserObject

import stripe

from users import models as users_models
from payments import models as payments_models

STRIPE_PUB_KEY = settings.STRIPE_PUB_KEY
STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY

def get_user_orders(request, user):
	user_orders_qs = portal_models.Order.objects.filter(user=user)
	if user_orders_qs.exists():
		return user_orders_qs
	return None


# <**************************************************************************>
# <*****                        CONSUMER VIEWS                          *****>
# <**************************************************************************>

# class CategoryListView(ListView):
# 	model = portal_models.Category


class CategoryDetailView(ListView):
	model = portal_models.Store
	template_name = 'portal/category_detail.html'
	paginate_by = 24

	def get_queryset(self, **kwargs):
		city_state = get_or_set_location(self.request)
		user_location = city_state["user_location"]
		slug = self.kwargs['slug']
		#Query Stores Nearby
		category_qs = portal_models.Category.objects.get(slug=slug)
		object_list = self.model.objects.annotate(distance = Distance("location", user_location)).order_by("distance").filter(status=2, category=category_qs)
		return object_list

	def get_context_data(self, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(**kwargs)
		context['category_list'] = portal_models.Category.objects.all()
		city_state = get_or_set_location(self.request)
		context['city'] = city_state["city"]
		context['state'] = city_state["state"]
		context['category'] = slug = self.kwargs['slug']
		return context


class SubcategoryDetailView(ListView):
	model = portal_models.Store
	template_name = 'portal/subcategory_detail.html'
	paginate_by = 24

	def get_queryset(self, **kwargs):
		city_state = get_or_set_location(self.request)
		user_location = city_state["user_location"]
		slug = self.kwargs['slug']
		#Query Stores Nearby
		subcategory_qs = portal_models.Subcategory.objects.get(slug=slug)
		object_list = self.model.objects.annotate(distance = Distance("location", user_location)).order_by("distance").filter(status=2, subcategory=subcategory_qs)
		return object_list

	def get_context_data(self, **kwargs):
		context = super(SubcategoryDetailView, self).get_context_data(**kwargs)
		context['category_list'] = portal_models.Category.objects.all()
		city_state = get_or_set_location(self.request)
		context['city'] = city_state["city"]
		context['state'] = city_state["state"]
		context['subcategory'] = slug = self.kwargs['slug']
		return context

class ConsumerStoreListView(ListView): #This needs to filter by user city or distance
	model = portal_models.Store
	template_name = 'portal/category_detail.html'
	paginate_by = 3

	def get_queryset(self):
		city_state = get_or_set_location(self.request)
		user_location = city_state["user_location"]
		#Query Stores Nearby
		object_list = self.model.objects.annotate(distance = Distance("location", user_location)).order_by("distance").filter(status=2)
		print(object_list)
		return object_list


	def get_context_data(self, **kwargs):
		context = super(ConsumerStoreListView, self).get_context_data(**kwargs)
		context['category_list'] = portal_models.Category.objects.all()
		city_state = get_or_set_location(self.request)
		context['city'] = city_state["city"]
		context['state'] = city_state["state"]

		#Check to see if follows exist
		try:
			store_connection = portal_models.FollowStore.objects.get(current_user = self.request.user)
			context['store_connections'] = store_connection.connections.all()
		except:
			pass

		return context


class ConsumerStoreDetailView(DetailView): #This needs to filter by user city or distance
	model = portal_models.Store
	template_name = 'portal/consumer/consumer_store_detail.html'

	def get_context_data(self, **kwargs):
		context = super(ConsumerStoreDetailView, self).get_context_data(**kwargs)


		try:
			if self.request.user.is_authenticated:
				store_connection_qs = portal_models.FollowStore.objects.filter(current_user=self.request.user)
				if store_connection_qs.exists():
					store_connection = portal_models.FollowStore.objects.get(current_user= self.request.user)
					context['store_connection_user'] = store_connection.connections.all()

				context['authenticated'] = True
			else:
				context['authenticated'] = False
		except:
			context['authenticated'] = False

		# context['related_stores'] = portal_models.Store.objects.filter(category=self.object.category, active=True).exclude(business_name=self.object.business_name)
		return context

	def get_object(self):
		obj = super(ConsumerStoreDetailView, self).get_object()
		obj.views += 1
		obj.save()
		return obj


# <**************************************************************************>
# <*****                      Visible by Merchants only                 *****>
# <**************************************************************************>

# Merchant Store

class MerchantStoreDetailView(LoginRequiredMixin, IsMerchantMixin, DetailView):
	model = portal_models.Store
	template_name = 'portal/merchant/merchant_detail_mpm.html'

	def get_context_data(self, **kwargs):
		self.object = self.get_object()

		context = super(MerchantStoreDetailView, self).get_context_data(**kwargs)
		store_pk = self.object.pk

		store_offer_qs = portal_models.StoreOffer.objects.filter(current_store=store_pk)
		if store_offer_qs.exists():
			store_offer = store_offer_qs.first()
			context['added_offers'] = store_offer.offers.all()

		context['offers'] = portal_models.Offer.objects.filter(author=self.request.user)
		return context

class MerchantStoreListView(LoginRequiredMixin, IsMerchantMixin, ListView):
	model = portal_models.Store
	template_name = 'portal/merchant/merchant_store_list.html'

	def get_queryset(self):
		store_list = portal_models.Store.objects.filter(merchant=self.request.user)
		return store_list

	def get_context_data(self, **kwargs):
		context = super(MerchantStoreListView, self).get_context_data(**kwargs)
		subscription_qs = payments_models.Subscription.objects.filter(user=self.request.user)

		if subscription_qs.exists():
			subscription = subscription_qs.first()
			context['subscription'] = subscription

		return context





class MerchantStoreUpdateView(LoginRequiredMixin, IsMerchantMixin, SuccessMessageMixin,  UpdateView):
	model = portal_models.Store
	form_class = MerchantStoreForm
	template_name = 'portal/merchant/merchant_store_update.html'
	success_message = "Store Updated"
	success_url = reverse_lazy('users:merchant_store_list')

	def form_valid(self, form):
		form.instance.status = 3
		return super(MerchantStoreUpdateView, self).form_valid(form)


class MerchantStoreDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = portal_models.Store
	template_name = 'portal/merchant/merchant_store_delete.html'
	# success_url = reverse_lazy('users:merchant_store_list')
	success_message = "Store Deleted"

	def get_context_data(self, **kwargs):
		context = super(MerchantStoreDeleteView, self).get_context_data(**kwargs)
		subscription_qs = payments_models.Subscription.objects.filter(user=self.request.user)
		if subscription_qs:
			context['subscription'] = subscription_qs.first()
		return context

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()

		stripe.api_key	= STRIPE_SECRET_KEY
		subscription_qs	= payments_models.Subscription.objects.filter(user=self.request.user)

		if subscription_qs.exists():
			subscription 		= subscription_qs.first()
			subscription_id 	= subscription.subscription_id

			if subscription.subscription_status == 'active':

				if self.request.user.merchant_profile.stores < subscription.subscription_quantity and self.request.user.merchant_profile.stores > 0:
					messages.success(self.request, 'Your store was deleted succesfully!')
					return redirect('payments:subscription_manage', slug=subscription.slug)

				elif self.request.user.merchant_profile.stores == 0:

					subscription = stripe.Subscription.delete(
						subscription_id,
						expand=['items', 'plan'],
					)

					sub, created                = payments_models.Subscription.objects.get_or_create(user=self.request.user)
					sub.subscription_id         = subscription['id']
					# sub.canceled_at             = subscription['canceled_at'] #TODO THIS IS CAUSING A PROBLEM ON SAVE
					sub.subscription_item_id    = subscription['items']['data'][0].id
					sub.subscription_quantity   = subscription['items']['data'][0].quantity
					sub.plan_id                 = subscription['plan']['id']
					sub.subscription_status     = subscription['status']

					if sub.invoice_upcoming == True:
						sub.invoice_upcoming = False
					else:
						pass

					sub.save()

					if sub.subscription_status == 'canceled':
						if self.request.user.merchant_profile.status == 'PENDING' or self.request.user.merchant_profile.status == 'APPROVED':
							merchant_profile_user = users_models.MerchantProfile.objects.get(user=self.request.user)
							merchant_profile_user.status = 'INITIAL'
							merchant_profile_user.save()
						else:
							pass

					messages.warning(self.request, 'You have deleted all your stores! Your subscription has been canceled')
					return redirect('payments:subscription_detail', slug=sub.slug)

				else:
					error_message = 'Something went wrong! Please contact support.'
					messages.warning(self.request, error_message)
					return redirect('users:userPage')

			elif subscription.subscription_status == 'trialing':
				messages.warning(self.request, 'You have deleted all your stores! Your subscption is still %s ' % sub.subscription_status)
				return redirect('users:merchant_store_list')

			else:
				error_message = 'Something went wrong! Please contact support.'
				messages.warning(self.request, error_message)
				return redirect('users:userPage')

		else:
			messages.success(self.request, 'The store was deleted!')
			return redirect('users:userPage')

# Merchant Offer


class MerchantOfferDetailView(LoginRequiredMixin, IsMerchantMixin, DetailView):
	model = portal_models.Offer
	template_name = 'portal/offer/merchant_offer_detail.html'


class MerchantOfferListView(LoginRequiredMixin, ListView):
	model = portal_models.Offer
	template_name = 'portal/offer/merchant_offer_list.html'

	def get_queryset(self):
		offer_list = portal_models.Offer.objects.filter(author=self.request.user)
		return offer_list

class MerchantOfferCreateView(LoginRequiredMixin, SuccessMessageMixin, IsMerchantMixin, CreateView):
	model = portal_models.Offer
	fields = [
		'title',
		'description',
		# 'end_date', #removed until we add the datepicker tool
	]
	template_name = 'portal/offer/merchant_offer_create.html'
	success_message = "Offer Created"
	success_url = reverse_lazy('users:merchant_offer_list')

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(MerchantOfferCreateView, self).form_valid(form)


class MerchantOfferUpdateView(LoginRequiredMixin, SuccessMessageMixin, IsMerchantMixin, UpdateView):
	model = portal_models.Offer
	fields = [
	'title',
	'description',
	'end_date',
	]
	template_name = 'portal/offer/merchant_offer_update.html'
	success_message = "Offer Updated"
	success_url = reverse_lazy('users:merchant_offer_list')

	def form_valid(self, form):
		form.instance.status = 4
		return super(MerchantOfferUpdateView, self).form_valid(form)


class MerchantOfferDeleteView(LoginRequiredMixin, IsMerchantMixin, SuccessMessageMixin, DeleteView):
	model = portal_models.Offer
	template_name = 'portal/offer/merchant_offer_delete.html'
	success_url = reverse_lazy('users:merchant_offer_list')
	success_message = "Offer Deleted"


def OfferLike(request):
	offer = get_object_or_404(portal_models.Offer, slug=request.POST.get('offer_slug'))
	offer.likes.add(request.user)
	return HttpResponseRedirect(offer.get_absolute_url())


class MerchantTestimonialListView(LoginRequiredMixin, IsMerchantMixin, ListView):
	model = portal_models.Testimonial
	template_name = 'portal/testimonials/merchant_testimonial_list.html'
	paginate_by = 2

	def get_queryset(self):
		object_list = portal_models.Testimonial.objects.filter(store__merchant=self.request.user)
		return object_list


class MerchantTestimonialCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = portal_models.Testimonial
	form_class = MerchantTestimonialForm
	template_name = 'portal/testimonials/merchant_testimonial_create.html'
	success_message = "Thank you for your input!"
	success_url = reverse_lazy('home-page')

	def get_context_data(self, **kwargs):
		context = super(MerchantTestimonialCreateView, self).get_context_data(**kwargs)
		store_qs = portal_models.Store.objects.filter(slug=self.kwargs['slug'], status=2)
		if store_qs.exists():
			context['store'] = store_qs.first()
		return context

	def form_valid(self, form):
		#Set testimonial author
		form.instance.author = self.request.user
		slug = self.kwargs['slug']
		try:
			store = portal_models.Store.objects.get(slug=slug, status=2)
			form.instance.store = store
		except:
			messages.warning(self.request, 'Error, Testimonail was unable to locate store')
			return redirect('home-page')


		return super(MerchantTestimonialCreateView, self).form_valid(form)

# <**************************************************************************>
# <*****                        STORE FUNCTIONS                          *****>
# <**************************************************************************>


def StoreChangeConnectionsAjax(request):
	if request.method == 'POST':
		store_pk = request.POST['store_pk']
		action = request.POST['action']

		print(store_pk)
		print(action)

		if action == 'add':
			store_connection_ajax = portal_models.Store.objects.get(pk=store_pk)
			portal_models.FollowStore.add_connection(request.user, store_connection_ajax)
			return HttpResponse('Success!')

		if action == 'remove':
			store_connection_ajax = portal_models.Store.objects.get(pk=store_pk)
			portal_models.FollowStore.remove_connection(request.user, store_connection_ajax)
			return HttpResponse('Success!')


def StoreOfferAjax(request):
	if request.method == 'POST':
		store_pk = request.POST['store_pk']
		offer_ajax_pk = request.POST['offer_pk']
		action = request.POST['action']

		print(store_pk)
		print(offer_ajax_pk)
		print(action)

		if action == 'add':
			store = portal_models.Store.objects.get(pk=store_pk)
			add_offer_ajax = portal_models.Offer.objects.get(pk=offer_ajax_pk)
			portal_models.StoreOffer.add_offer(store, add_offer_ajax)
			return HttpResponse('Success!')

		if action == 'remove':
			store = portal_models.Store.objects.get(pk=store_pk)
			add_offer_ajax = portal_models.Offer.objects.get(pk=offer_ajax_pk)
			portal_models.StoreOffer.remove_offer(store, add_offer_ajax)
			return HttpResponse('Success!')
