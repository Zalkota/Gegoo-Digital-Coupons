from django.urls import path

from portal import views as portal_views

app_name = 'portal'

urlpatterns = [

    path('<slug:slug>', portal_views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/all/', portal_views.CategoryListView.as_view(), name='category_list'),
    path('category/<category>/<slug:slug>', portal_views.SubcategoryDetailView.as_view(), name='subcategory_detail'),


    #Consumer Store Views
    path('store/<slug:slug>/', portal_views.StoreDetailView.as_view(), name='store_detail'),


    # Merchant Store Views
    path('my-store/<slug:slug>/', portal_views.MerchantStoreDetailView.as_view(), name='merchant_store_detail'),
    path('my-stores/', portal_views.MerchantStoreListView.as_view(), name='merchant_store_list'),
    path('my-store/create', portal_views.MerchantStoreCreateView.as_view(), name='merchant_store_create'),
    path('my-store/<slug:slug>/update', portal_views.MerchantStoreUpdateView.as_view(), name='store_update'),
    path('my-store/<slug:slug>/delete', portal_views.MerchantStoreDeleteView.as_view(), name='store_delete'),


    path('my-subscription/', portal_views.MerchantSubscriptionsView.as_view(), name='subscription_list'),
    path('mystores/', portal_views.StoreList, name='store_function'),


    #Consumer Offer Views
    path('offers', portal_views.MerchantOfferListView.as_view(), name='offer_list'),
    path('offer/<slug:slug>/', portal_views.MerchantOfferDetailView.as_view(), name='offer_detail'),


    #Merchant Offer Views
    path('offer/create', portal_views.MerchantOfferCreateView.as_view(), name='merchant_offer_create'),
    path('offer/<slug:slug>/update', portal_views.MerchantOfferUpdateView.as_view(), name='merchant_offer_update'),
    path('offer/<slug:slug>/delete', portal_views.MerchantOfferDeleteView.as_view(), name='merchant_offer_delete'),
    path('offer/like', portal_views.OfferLike, name='offer_like'),
    path('store/<int:store_id>/add/<slug:offer_id>', portal_views.OfferAdd, name='offer_add'),
    path('store/<int:store_id>/remove/<slug:offer_id>', portal_views.OfferRemove, name='offer_remove'),


]
