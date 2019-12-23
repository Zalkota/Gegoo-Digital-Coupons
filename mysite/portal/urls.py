from django.urls import path
from .views import (
    #CouponDetailView,
    MerchantDetailView,
    CategoryDetailView,
    CategoryListView,
    FAQView,
    FAQAccountView,
    FAQPaymentView,
    FAQAcceptableOffersView,
    FAQDetailView,
)


app_name = 'portal'

urlpatterns = [

    path('/<category>/<subcategory>/<name>/<ref_code>', MerchantDetailView.as_view(), name='merchant_detail'),
    path('category/<name>', CategoryDetailView.as_view(), name='category_detail'),
    path('category/all/', CategoryListView.as_view(), name='category_list'),
    # path('/category/', CategoryListView.as_view(), name='category-list'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('faq/<int:pk>', FAQDetailView.as_view(), name='faq-detail'),
    path('faq/accounts', FAQAccountView.as_view(), name='faq-account'),
    path('faq/payment', FAQPaymentView.as_view(), name='faq-payment'),
    path('faq/acceptable-offers', FAQAcceptableOffersView.as_view(), name='faq-acceptable-offers'),
]
