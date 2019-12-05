from django.conf.urls import url
from django.urls import path
from . import views
from .views import  Home


urlpatterns = [

    #Users
    path('home/', Home.as_view(), name='home'),


]
