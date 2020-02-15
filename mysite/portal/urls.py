from django.urls import path

from portal import views as portal_views

app_name = 'portal'

urlpatterns = [

    path('<slug:slug>', portal_views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/all/', portal_views.CategoryListView.as_view(), name='category_list'),
    path('category/<category>/<slug:slug>', portal_views.SubcategoryDetailView.as_view(), name='subcategory_detail'),

    #Consumer Store Views
    path('store/<slug:slug>/', portal_views.MerchantStoreDetailView.as_view(), name='store_detail'),

    #Consumer Views
    path('stores/', portal_views.ConsumerStoreListView.as_view(), name='consumer_store_list'),
    path('store/<slug:slug>', portal_views.ConsumerStoreDetailView.as_view(), name='consumer_store_detail'),

    #Connections
    path('store-connect/', portal_views.StoreChangeConnectionsAjax, name='store_change_connections'),  
    path('offer-connect/', portal_views.StoreOfferAjax, name='offer_change_connections')

]
