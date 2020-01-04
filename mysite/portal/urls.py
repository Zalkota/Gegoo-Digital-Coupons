from django.urls import path
from .views import (
    #CouponDetailView,
    MerchantDetailView,
    CategoryDetailView,
    CategoryListView,
)


app_name = 'portal'

urlpatterns = [

    path('<category>/<subcategory>/<name>/<ref_code>', MerchantDetailView.as_view(), name='merchant_detail'),
    path('category/<name>', CategoryDetailView.as_view(), name='category_detail'),
    path('category/all/', CategoryListView.as_view(), name='category_list'),
    # path('/category/', CategoryListView.as_view(), name='category-list'),
<<<<<<< HEAD
=======

>>>>>>> alpha
]
