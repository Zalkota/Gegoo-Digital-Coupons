from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet

from shoppingcart.models import Item, Category
from .forms import FacetedItemSearchForm

#class HomeView(TemplateView):
#  template_name = "home.html"

#class ProductView(DetailView):
#  template_name = "product.html"
#  model = Product

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('query',''))[:5]
    s = []
    for result in sqs:
        d = {"value": result.title, "data": result.object.slug}
        s.append(d)
    output = {'suggestions': s}
    return JsonResponse(output)


class FacetedSearchView(BaseFacetedSearchView):
    form_class = FacetedItemSearchForm
    facet_fields = ['category']
    template_name = 'search/search_result.html'

    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['advert_list'] = Item.objects.all()[:4]
        return context
