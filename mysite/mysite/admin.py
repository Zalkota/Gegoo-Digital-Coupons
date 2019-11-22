from django.contrib import admin
from .models import Contact
from shoppingcart.models import Promotion



admin.site.register(Contact)
admin.site.register(Promotion)
