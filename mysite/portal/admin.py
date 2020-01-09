from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Store, Offer, Promotion, Images, Category, Subcategory, Tag, About
from location.models import store_address
# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin

from cities_light.models import City, Region



class AboutAdmin(ImportExportModelAdmin):
     model= About
     filter_horizontal = ('images',) #If you don't specify this, you will get a multiple select widget.

class StoreAddressInline(admin.TabularInline):
    model = store_address

class StoreAdmin(admin.ModelAdmin):
    search_fields = ['city__name', 'business_name']
    autocomplete_fields = ['city']
    list_display = ('business_name', 'city', 'category', 'subcategory', 'active')
    inlines = [
        StoreAddressInline,
    ]

class OfferAdmin(admin.ModelAdmin):
    autocomplete_fields = ['store']

# class LocationAdmin(admin.ModelAdmin):
#     search_fields = ['city__name', 'state__name', 'user__username']
#     autocomplete_fields = ['city', 'state']



admin.site.register(Store, StoreAdmin)
admin.site.register(Offer)
#admin.site.register(LocationAdmin)
admin.site.register(Promotion)
admin.site.register(Images)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Tag)
admin.site.register(About, AboutAdmin)
