from haystack.forms import FacetedSearchForm
from portal.models import Category, Subcategory, Offer


class FacetedOfferSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        data = dict(kwargs.get("data", []))
        self.category = data.get('category', [])
        self.subcategory = data.get('subcategory', [])
        self.city = data.get('city', [])
        super(FacetedOfferSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(FacetedOfferSearchForm, self).search()
        if self.category:
            query = None
            for category in self.category:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(category)
            sqs = sqs.narrow(u'category_exact:%s' % query)

        if self.subcategory:
            query = None
            for subcategory in self.subcategory:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(subcategory)
            sqs = sqs.narrow(u'subcategory_exact:%s' % query)

        if self.city:
            query = None
            for city in self.city:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(city)
            sqs = sqs.narrow(u'city_exact:%s' % query)

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
