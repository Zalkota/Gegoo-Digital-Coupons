from django.conf.urls import url
from django.urls import path
from . import views
from .views import SearchAddress


urlpatterns = [

    #Users
    # path('home/', Home.as_view(), name='home'),
    path('dashboard/location/search/', SearchAddress, name='search_address'),


]
