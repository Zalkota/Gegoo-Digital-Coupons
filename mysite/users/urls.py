from django.conf.urls import url
from django.urls import path
from . import views
from .views import  UserRedirectView, UserUpdateView, RedirectProfileView, userPage, userLocaton, MerchantSignUpView, userRewards, userFavorites, userMerchants



urlpatterns = [



    path('dashboard/', userPage.as_view(), name='userPage'),


    #Consumer User Profile
    path('dashboard/location/', userLocaton.as_view(), name='user_location'),
    path('dashboard/rewards/', userRewards.as_view(), name='user_rewards'),
    path('dashboard/favorite-offers/', userFavorites.as_view(), name='user_favorites'),
    path('dashboard/merchant-offers/', userFavorites.as_view(), name='user_merchants'),
    url(r'^users/~redirect/$', UserRedirectView.as_view(), name='redirect'),
    url(r'^users/~update/$', UserUpdateView.as_view(), name='update'),
    url(r'^users/redirectprofile/$', RedirectProfileView.as_view(), name='redirectprofile'),


    #User Signup Forms
    path('merchant-signup/', MerchantSignUpView.as_view(), name='merchant-signup'),
    # path('consumer-signup/', ConsumerSignUpView.as_view(), name='consumer-signup'),


]
