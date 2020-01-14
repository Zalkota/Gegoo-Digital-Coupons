from django.conf.urls import url
from django.urls import path
from users import views as users_views
from users import views_approval as users_approval_views

urlpatterns = [



    path('dashboard/', users_views.userPage.as_view(), name='userPage'),

    #Consumer User Profile
    path('dashboard/location/', users_views.userLocaton.as_view(), name='user_location'),
    path('dashboard/rewards/', users_views.userRewards.as_view(), name='user_rewards'),
    path('dashboard/favorite-offers/', users_views.userFavorites.as_view(), name='user_favorites'),
    path('dashboard/merchant-offers/', users_views.userFavorites.as_view(), name='user_merchants'),
    url(r'^users/~redirect/$', users_views.UserRedirectView.as_view(), name='redirect'),
    url(r'^users/~update/$', users_views.UserUpdateView.as_view(), name='user_profile_update'),
    url(r'^users/redirectprofile/$', users_views.RedirectProfileView.as_view(), name='redirectprofile'),


    #Merchant Signup Forms
    path('merchant-signup/', users_views.MerchantSignUpView.as_view(), name='merchant-signup'),

    # path('consumer-signup/', ConsumerSignUpView.as_view(), name='consumer-signup'),

    #Merchant Approval Views
    path('my-profile/<int:pk>/update', users_approval_views.MerchantProfileUpdateView.as_view(), name='merchant_profile_update'),
    path('form-submission/',  users_approval_views.MerchantProfileFormLandingView, name='merchant-profile-landing-page'),

]
