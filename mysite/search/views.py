from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet

from portal.models import Offer, Category, Store
from .forms import FacetedOfferSearchForm

#Location
from location.functions import get_or_set_location
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

#class HomeView(TemplateView):
#  template_name = "home.html"

#class ProductView(DetailView):
#  template_name = "product.html"
#  model = Product

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('query',''))[:5]
    s = []
    for result in sqs:
        d = {"value": result.business_name, "data": result.slug}
        s.append(d)
    output = {'suggestions': s}
    return JsonResponse(output)


class FacetedSearchView(BaseFacetedSearchView):
    form_class = FacetedOfferSearchForm
    facet_fields = ['category', 'subcategory', 'city']
    template_name = 'search/search_result.html'
    context_object_name = 'object_list'
    #
    #
    # def get_queryset(self):
    #     objects = super(FacetedSearchView, self).get_results(self)
    #     city_state = get_or_set_location(self.request)
    #     user_location = city_state["user_location"]
    #     return self.objects.annotate(distance = Distance("location", user_location)).order_by("distance").filter(status=2)[0:8]


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        city_state = get_or_set_location(self.request)
        user_location = city_state["user_location"]
        try:
            context['advert_list'] = Store.objects.annotate(distance = Distance("location", user_location)).order_by("distance").filter(status=2)[0:4]
        except:
            context['advert_list'] = Store.objects.filter(city='Novi', state='Michigan')[0:8]
        return context
