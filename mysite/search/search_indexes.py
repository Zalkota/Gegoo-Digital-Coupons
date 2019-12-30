import datetime
from django.utils import timezone
from haystack import indexes
from haystack.fields import CharField

from portal.models import Offer

class OfferIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
    document=True, use_template=True,
    template_name='/home/dom/Desktop/projects/estore/mysite/templates/search/item_text.txt')

    title = indexes.EdgeNgramField(model_attr='title')
    description = indexes.EdgeNgramField(model_attr="description", null=True)
    timestamp = indexes.DateTimeField(model_attr='timestamp')

    category = indexes.CharField(model_attr='category', faceted=True)

    # for auto complete
    content_auto = indexes.EdgeNgramField(model_attr='title')

    # Spelling suggestions
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Offer

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(timestamp__lte=timezone.now())
