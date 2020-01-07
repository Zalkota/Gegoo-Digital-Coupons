from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

## DEBUG:
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from portal import models as portal_models
from django.views.generic import ListView, DetailView, View, CreateView, DeleteView, UpdateView
# Create your views here.

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
latitude = 42.637740
longitude = -83.363546
user_location = Point(longitude, latitude, srid=4326)


def get_user_orders(request, user):
	user_orders_qs = portal_modedls.Order.objects.filter(user=user)
	if user_orders_qs.exists():
		return user_orders_qs
	return None

class CategoryListView(ListView):
	model = portal_models.Category


class CategoryDetailView(View):

	def get(self, *args, **kwargs):
		try:
			category = portal_models.Category.objects.get(name=self.kwargs['name'])
			category_nearby_stores = portal_models.Store.objects.filter(category=category).annotate(distance = Distance("location", user_location)).order_by("distance")[0:9]
			all_categories = portal_models.Category.objects.all()

			context = {
			'category': category,
			'category_nearby_stores': category_nearby_storess,
			'all_categories': all_categories,
			}
			return render(self.request, "portal/category_detail.html", context)

		except ObjectDoesNotExist:
			messages.info(self.request, "Error contact admin")
			return redirect("home-page")

class StoreListView(ListView):
	model = portal_models.Store
	template_name = 'store/store_list.html'

	def get_queryset(self):
		store_list = portal_models.Store.objects.filter(merchant=self.request.user)
		return store_list

class StoreDetailView(DetailView):
	model = portal_models.Store
	template_name = 'store/store_detail.html'

	def get_context_data(self, **kwargs):
		context = super(StoreDetailView, self).get_context_data(**kwargs)
		context['offers'] = portal_models.Offer.objects.filter(author=self.request.user).exclude(slug__in=self.object.offers.all().values_list('slug'))
		return context

class StoreCreateView(CreateView):
	model = portal_models.Store
	fields = [
		'business_name',
		'title',
		'description',
	]
	
	template_name = 'store/store_create.html'

	def form_valid(self, form):
		form.instance.merchant = self.request.user
		return super(StoreCreateView, self).form_valid(form)

class StoreUpdateView(UpdateView):
    model = portal_models.Store
    fields = [
		'business_name',
		'title',
		'description',
    ]

    template_name = 'store/store_update.html'

class StoreDeleteView(DeleteView):
    model = portal_models.Offer
    template_name = 'store/store_delete.html'
    success_url = reverse_lazy('portal:store_list')

class OfferListView(ListView):
	model = portal_models.Offer
	template_name = 'offer/offer_list.html'

	def get_queryset(self):
		offer_list = portal_models.Offer.objects.filter(author=self.request.user)
		return offer_list

class OfferDetailView(DetailView):
	model = portal_models.Offer
	template_name = 'offer/offer_detail.html'

class OfferCreateView(CreateView):
	model = portal_models.Offer
	fields = [
		'title',
		'description',
		'end_date',
	]
	
	template_name = 'offer/offer_create.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(OfferCreateView, self).form_valid(form)

class OfferUpdateView(UpdateView):
    model = portal_models.Offer
    fields = [
		'title',
		'description',
		'end_date',
    ]

    template_name = 'offer/offer_update.html'

class OfferDeleteView(DeleteView):
    model = portal_models.Offer
    template_name = 'offer/offer_delete.html'
    success_url = reverse_lazy('portal:offer_list')

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
