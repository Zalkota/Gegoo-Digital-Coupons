from django.urls import path
from .views import (
    ItemDetailView,
    CheckoutView,
    OrderReviewView,
    HomeView,
    OrderSummaryView,
    OrderDetailView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    ItemListHomeView
)

app_name = 'shoppingcart'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ItemListHomeView.as_view(), name='products'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-review/<ref_code>/', OrderReviewView.as_view(), name='order-review'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('order-detail/<ref_code>/', OrderDetailView.as_view(), name='order'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]
