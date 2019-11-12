from haystack.forms import FacetedSearchForm
from shoppingcart.models import Category, Item


class FacetedItemSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        data = dict(kwargs.get("data", []))
        self.categories = data.get('category', [])
        super(FacetedItemSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(FacetedItemSearchForm, self).search()
        if self.categories:
            query = None
            for category in self.categories:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(category)
            sqs = sqs.narrow(u'category_exact:%s' % query)
        return sqs
  #if self.brands:
  #query = None
  #for brand in self.brands:
  #if query:
  #query += u' OR '
  #else:
  #query = u''
  #query += u'"%s"' % sqs.query.clean(brand)
  #sqs = sqs.narrow(u'brand_exact:%s' % query)
  #return sqs
