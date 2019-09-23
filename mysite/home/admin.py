from django.contrib import admin
from .models import Service, Contact, Review, Page, Coupon, Product, Furnace, AirConditioning


admin.site.register(Review)
admin.site.register(Page)
admin.site.register(Service)
admin.site.register(Coupon)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Furnace)
admin.site.register(AirConditioning)
