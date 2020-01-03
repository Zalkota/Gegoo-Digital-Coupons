from django.conf.urls import url
from django.urls import path
from . import views
from .views import  UserRedirectView, UserUpdateView, RedirectProfileView, userPage, userLocaton, userRewards


urlpatterns = [

    #Users
    path('dashboard/', userPage.as_view(), name='userPage'),
    path('dashboard/location/', userLocaton.as_view(), name='user_location'),
    path('dashboard/rewards/', userRewards.as_view(), name='user_rewards'),
    url(r'^users/~redirect/$', UserRedirectView.as_view(), name='redirect'),
    url(r'^users/~update/$', UserUpdateView.as_view(), name='update'),
    url(r'^users/redirectprofile/$', RedirectProfileView.as_view(), name='redirectprofile'),
    # path('users/update/image/', add_image, name='update_image'),


]
