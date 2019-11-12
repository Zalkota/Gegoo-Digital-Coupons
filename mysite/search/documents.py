from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry

from shoppingcart.models import Item

Items = Index('Items')

@registry.register_document
class ItemDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'items'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}


    class Django:
        model = Item # The model associated with this Document

        fields = [
            'title',
            'description',
        ]


        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000
