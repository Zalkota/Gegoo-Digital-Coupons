import datetime
from django.utils import timezone
from haystack import indexes
from haystack.fields import CharField

from portal.models import Store



class StoreIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
    document=True, use_template=True,
    template_name='/app/templates/search/item_text.txt')
    # /templates/search/item_text.txt

    business_name = indexes.EdgeNgramField(model_attr='business_name')
    description = indexes.EdgeNgramField(model_attr="description", null=True)

    updated_at = indexes.DateTimeField(model_attr='updated_at')

    #Faceted Objects
    category = indexes.CharField(model_attr='category', faceted=True)
    subcategory = indexes.CharField(model_attr='subcategory', faceted=True)
    city = indexes.CharField(model_attr='city', faceted=True)

    # for auto complete
    content_auto = indexes.EdgeNgramField(model_attr='business_name')

    # Spelling suggestions
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Store

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(updated_at__lte=timezone.now())
        # city_state = get_or_set_location(self.request)
        # user_location = city_state["user_location"]
        # return self.get_model().objects.annotate(distance = Distance("location", user_location)).order_by("distance").filter(status=2)[0:8]
