from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Store, Offer, Images, Category, Subcategory, Tag, Testimonial, FollowStore, StoreOffer
from users.models import MerchantProfile, User
# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin

from cities_light.models import City, Region



    # autocomplete_fields = ['city']

class StoreAdmin(admin.ModelAdmin):
    search_fields = ['city', 'business_name']
    list_display = ('business_name', 'city', 'state', 'category', 'subcategory', 'subscription_status', 'status', 'merchant')
    # inlines = [
    #     UserProfileInline,
    # ]

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')


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
admin.site.register(Images)
admin.site.register(Category)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Tag)
admin.site.register(FollowStore)
admin.site.register(StoreOffer)
