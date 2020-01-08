from django.urls import path

from portal import views as portal_views


app_name = 'portal'

urlpatterns = [

    path('category/<name>', portal_views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/all/', portal_views.CategoryListView.as_view(), name='category_list'),

    # Store Views
    path('stores', portal_views.StoreListView.as_view(), name='store_list'),
    path('store/create', portal_views.StoreCreateView.as_view(), name='store_create'),
    path('store/<slug:slug>/', portal_views.StoreDetailView.as_view(), name='store_detail'),
    path('store/<slug:slug>/update', portal_views.StoreUpdateView.as_view(), name='store_update'),
    path('store/<slug:slug>/delete', portal_views.StoreDeleteView.as_view(), name='store_delete'),

    path('mystores/', portal_views.StoreList, name='store_function'),

    # Offer Views
    path('offers', portal_views.OfferListView.as_view(), name='offer_list'),
    path('offer/create', portal_views.OfferCreateView.as_view(), name='offer_create'),
    path('offer/<slug:slug>/', portal_views.OfferDetailView.as_view(), name='offer_detail'),
    path('offer/<slug:slug>/update', portal_views.OfferUpdateView.as_view(), name='offer_update'),
    path('offer/<slug:slug>/delete', portal_views.OfferDeleteView.as_view(), name='offer_delete'),
    path('offer/like', portal_views.OfferLike, name='offer_like'),
    path('store/<int:store_id>/add/<slug:offer_id>', portal_views.OfferAdd, name='offer_add'),
    path('store/<int:store_id>/remove/<slug:offer_id>', portal_views.OfferRemove, name='offer_remove'),
]
