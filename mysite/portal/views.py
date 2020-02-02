# <**************************************************************************>
# <*****                         IMPORTS                                *****>
# <**************************************************************************>
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

## DEBUG:
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
from .forms import MerchantStoreForm
from users.decorators import IsMerchantMixin, IsUserObject

from users import models as users_models

def get_user_orders(request, user):
	user_orders_qs = portal_modedls.Order.objects.filter(user=user)
	if user_orders_qs.exists():
		return user_orders_qs
	return None

class CategoryListView(ListView):
	model = portal_models.Category


class CategoryDetailView(DetailView):
	model = portal_models.Category
	template_name = 'portal/category_detail.html'

	def get_context_data(self, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(**kwargs)
		context['category_list'] = portal_models.Category.objects.all()
		return context


class SubcategoryDetailView(DetailView):
	model = portal_models.Subcategory
	template_name = 'portal/subcategory_detail.html'

	def get_context_data(self, **kwargs):
		context = super(SubcategoryDetailView, self).get_context_data(**kwargs)
		context['category_list'] = portal_models.Category.objects.all()
		return context

	# def get(self, *args, **kwargs):
	# 	try:
	# 		subcategory = portal_models.Subcategory.objects.get()
	# 		#category_nearby_stores = portal_models.Store.objects.filter(category=category).annotate(distance = Distance("location", user_location)).order_by("distance")[0:9]
	# 		#all_categories = portal_models.Category.objects.all()
	# 		print(category_list)
	# 		context = {
	# 		'category_list': category_list,
	# 		#'category_nearby_stores': category_nearby_storess,
	# 		#'all_categories': all_categories,
	# 		}
	# 		return render(self.request, "portal/category_detail.html", context)
	#
	# 	except ObjectDoesNotExist:
	# 		messages.info(self.request, "Error contact admin")
	# 		return redirect("home-page")


class ConsumerStoreDetailView(DetailView): #This needs to filter by user city or distance
	model = portal_models.Store
<<<<<<< HEAD
	template_name = 'portal/consumer/consumer_store_detail.html'
=======
	template_name = 'portal/store/merchant_store_detail.html'
>>>>>>> subscription

	def get_context_data(self, **kwargs):
		context = super(StoreDetailView, self).get_context_data(**kwargs)
		context['related_stores'] = portal_models.Store.objects.filter(category=self.object.category, active=True).exclude(business_name=self.object.business_name)
		return context


# <**************************************************************************>
# <*****                      Visible by Merchants only                 *****>
# <**************************************************************************>

# Merchant Store

class MerchantStoreDetailView(LoginRequiredMixin, DetailView):
	model = portal_models.Store
<<<<<<< HEAD
	template_name = 'portal/merchant/merchant_store_detail.html'
=======
	template_name = 'portal/store/merchant_store_detail.html'
>>>>>>> subscription

	# def get_object(self):
	# 	obj = super(MerchantStoreDetailView, self).get_object()
	# 	obj.views += 1
	# 	obj.save()
	# 	return obj

	def get_context_data(self, **kwargs):
		context = super(MerchantStoreDetailView, self).get_context_data(**kwargs)
		context['offers'] = portal_models.Offer.objects.filter(author=self.request.user).exclude(slug__in=self.object.offers.all().values_list('slug'))
		return context


class MerchantStoreListView(LoginRequiredMixin, ListView):
	model = portal_models.Store
	template_name = 'portal/merchant/merchant_store_list.html'

	def get_queryset(self):
		store_list = portal_models.Store.objects.filter(merchant=self.request.user)
		return store_list


class MerchantStoreCreateView(LoginRequiredMixin, CreateView):
	model = portal_models.Store
	form_class = MerchantStoreForm
	template_name = 'portal/merchant/merchant_store_create.html'
	success_message = "Store Created"
	success_url = reverse_lazy('users:merchant_store_list')

	def form_valid(self, form):
		user = self.request.user
		user.status = 'PENDING'

		user.save()

		form.instance.merchant = self.request.user
		return super(MerchantStoreCreateView, self).form_valid(form)


class MerchantStoreUpdateView(LoginRequiredMixin, UpdateView):
	model = portal_models.Store
	form_class = MerchantStoreForm
	template_name = 'portal/merchant/merchant_store_update.html'
	success_message = "Store Updated"
	success_url = reverse_lazy('users:merchant_store_list')


class MerchantStoreDeleteView(LoginRequiredMixin, DeleteView):
<<<<<<< HEAD
	model = portal_models.Store
	template_name = 'portal/merchant/merchant_store_delete.html'
	success_url = reverse_lazy('users:merchant_store_list')
	success_message = "Store Deleted"


# Merchant Offer


class MerchantOfferDetailView(LoginRequiredMixin, IsMerchantMixin, DetailView):
	model = portal_models.Offer
	template_name = 'portal/offer/merchant_offer_detail.html'

=======
    model = portal_models.Store
    template_name = 'portal/store/merchant_store_delete.html'
    success_url = reverse_lazy('portal:merchant_store_list')
>>>>>>> subscription

class MerchantOfferListView(LoginRequiredMixin, ListView):
	model = portal_models.Offer
	template_name = 'portal/offer/merchant_offer_list.html'

	def get_queryset(self):
		offer_list = portal_models.Offer.objects.filter(author=self.request.user)
		return offer_list


class MerchantOfferCreateView(LoginRequiredMixin, IsMerchantMixin, CreateView):
	model = portal_models.Offer
	fields = [
		'title',
		'description',
		'end_date',
	]
	template_name = 'portal/offer/merchant_offer_create.html'
	success_message = "Offer Created"

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(MerchantOfferCreateView, self).form_valid(form)


class MerchantOfferUpdateView(LoginRequiredMixin, IsMerchantMixin, UpdateView):
	model = portal_models.Offer
	fields = [
	'title',
	'description',
	'end_date',
	]
	template_name = 'portal/offer/merchant_offer_update.html'
	success_message = "Offer Updated"


class MerchantOfferDeleteView(LoginRequiredMixin, IsMerchantMixin, DeleteView):
	model = portal_models.Offer
	template_name = 'portal/offer/merchant_offer_delete.html'
	success_url = reverse_lazy('users:offer_list')
	success_message = "Offer Deleted"


def OfferLike(request):
	offer = get_object_or_404(portal_models.Offer, slug=request.POST.get('offer_slug'))
	offer.likes.add(request.user)
	return HttpResponseRedirect(offer.get_absolute_url())

def OfferAdd(request, store_id, offer_id):
	store = portal_models.Store.objects.get(id=store_id)
	store.offers.add(offer_id)
	return HttpResponseRedirect(store.get_absolute_url())

def OfferRemove(request, store_id, offer_id):
	store = portal_models.Store.objects.get(id=store_id)
	store.offers.remove(offer_id)
	return HttpResponseRedirect(store.get_absolute_url())

# Testimonails

class MerchantTestimonialListView(LoginRequiredMixin, IsMerchantMixin, ListView):
	model = portal_models.Testimonial
	template_name = 'portal/testimonials/merchant_testimonial_list.html'
	paginate_by = 2

	def get_queryset(self):
		object_list = portal_models.Testimonial.objects.filter(store__merchant=self.request.user)
		return object_list

# <**************************************************************************>
# <*****                        CONSUMER VIEWS                          *****>
# <**************************************************************************>

class ConsumerStoreListView(ListView):
	model = portal_models.Store
	template_name = 'portal/consumer/consumer_store_list.html'

	def get_queryset(self):
		store_list = portal_models.Store.objects.all()
		return store_list

	def get_context_data(self, **kwargs):
		context = super(ConsumerStoreListView, self).get_context_data(**kwargs)
		context['trending_stores'] = portal_models.Store.objects.all().order_by('-views')[0:4]
		return context


class ConsumerStoreDetailView(DetailView):
	model = portal_models.Store
	template_name = 'portal/consumer/consumer_store_detail.html'

	def get_object(self):
		obj = super(ConsumerStoreDetailView, self).get_object()
		obj.views += 1
		obj.save()
		return obj
