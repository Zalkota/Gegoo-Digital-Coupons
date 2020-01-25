from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Store, Offer, PromotionalVideo, Images, Category, Subcategory, Tag, Testimonial
from location.models import StoreLocation
# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin

from cities_light.models import City, Region



class StoreLocationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['city']

# class StoreLocationInline(admin.TabularInline):
#     model = StoreLocation
#     autocomplete_fields = ['city']

class StoreAdmin(admin.ModelAdmin):
    search_fields = ['city', 'business_name']
    list_display = ('business_name', 'city', 'category', 'subcategory', 'active', 'status')
    # inlines = [
    #     StoreLocationInline,
    # ]

class OfferAdmin(admin.ModelAdmin):
    autocomplete_fields = ['store']

# class LocationAdmin(admin.ModelAdmin):
#     search_fields = ['city__name', 'state__name', 'user__username']
#     autocomplete_fields = ['city', 'state']

class TestimonialAdmin(admin.ModelAdmin):
    list_display            = ('author', 'store', 'rating')
    list_filter             = ('created_at', 'updated_at')
    search_fields           = ('author', 'store')
    date_hierarchy          = ('created_at')


admin.site.register(Store, StoreAdmin)
admin.site.register(Offer)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(StoreLocation, StoreLocationAdmin)
admin.site.register(Images)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Tag)
admin.site.register(PromotionalVideo)
