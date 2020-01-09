from django.urls import path

from portal import views as portal_views


app_name = 'portal'

urlpatterns = [

    path('category/<name>', portal_views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/all/', portal_views.CategoryListView.as_view(), name='category_list'),

    # Store Views
    path('my-stores/', portal_views.MerchantStoreListView.as_view(), name='merchant_store_list'),
    path('my-store/create', portal_views.MerchantStoreCreateView.as_view(), name='merchant_store_create'),
    path('my-store/<slug:slug>/', portal_views.MerchantStoreDetailView.as_view(), name='merchant_store_detail'),
    path('my-store/<slug:slug>/update', portal_views.MerchantStoreUpdateView.as_view(), name='merchant_store_update'),
    path('my-store/<slug:slug>/delete', portal_views.MerchantStoreDeleteView.as_view(), name='merchant_store_delete'),

    # Offer Views
    path('my-offers/', portal_views.MerchantOfferListView.as_view(), name='merchant_offer_list'),
    path('my-offer/create', portal_views.MerchantOfferCreateView.as_view(), name='merchant_offer_create'),
    path('my-offer/<slug:slug>/', portal_views.MerchantOfferDetailView.as_view(), name='merchant_offer_detail'),
    path('my-offer/<slug:slug>/update', portal_views.MerchantOfferUpdateView.as_view(), name='merchant_offer_update'),
    path('my-offer/<slug:slug>/delete', portal_views.MerchantOfferDeleteView.as_view(), name='merchant_offer_delete'),
    path('my-offer/like', portal_views.OfferLike, name='offer_like'),
    path('my-store/<int:store_id>/add/<int:offer_id>', portal_views.OfferAdd, name='offer_add'),
    path('my-store/<int:store_id>/remove/<int:offer_id>', portal_views.OfferRemove, name='offer_remove'),

    #Consumer Views
    path('stores/', portal_views.ConsumerStoreListView.as_view(), name='consumer_store_list'),
    path('store/<slug:slug>', portal_views.ConsumerStoreDetailView.as_view(), name='consumer_store_detail')
]
