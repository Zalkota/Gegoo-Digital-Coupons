from django.urls import path
from .views import (
    #CouponDetailView,
    MerchantDetailView,
)


app_name = 'portal'

urlpatterns = [

    path('<state>/<city>/<category>/<subcategory>/<name>/<ref_code>', MerchantDetailView.as_view(), name='merchant-detail'),

]
