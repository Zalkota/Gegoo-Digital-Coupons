from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [

    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
        url(r'^redirectprofile/$', views.RedirectProfileView.as_view(), name='redirectprofile'),


    #Profile Image
    path('users/update/image/', add_image, name='update_image'),


]
