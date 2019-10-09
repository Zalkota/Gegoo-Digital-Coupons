from django.conf.urls import url
from django.urls import path
from . import views
from .views import  UserDetailView, UserRedirectView, UserUpdateView, RedirectProfileView, userPage, add_image, user_jobs_view


urlpatterns = [

    #Users
    url(r'^profile/$', userPage, name='userPage'),
    url(r'^users/~redirect/$', UserRedirectView.as_view(), name='redirect'),
    url(r'^users/(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^users/~update/$', UserUpdateView.as_view(), name='update'),
    url(r'^users/redirectprofile/$', RedirectProfileView.as_view(), name='redirectprofile'),
    path('users/update/image/', add_image, name='update_image'),
    path('orders/', user_jobs_view, name='user_jobs'),

    #Profile Image
    path('users/update/image/', add_image, name='update_image'),


]
