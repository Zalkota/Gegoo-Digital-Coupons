from django.conf.urls import url
from django.urls import path
from . import views
from .views import  UserRedirectView, UserUpdateView, RedirectProfileView, userPage


urlpatterns = [

    #Users
    path('dashboard/', userPage.as_view(), name='userPage'),
    url(r'^users/~redirect/$', UserRedirectView.as_view(), name='redirect'),
    url(r'^users/~update/$', UserUpdateView.as_view(), name='update'),
    url(r'^users/redirectprofile/$', RedirectProfileView.as_view(), name='redirectprofile'),
    # path('users/update/image/', add_image, name='update_image'),


]
