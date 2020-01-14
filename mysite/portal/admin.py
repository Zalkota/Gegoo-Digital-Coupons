from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Store, Offer, Address, Promotion, Images, Category, Tag, About, Testimonial
# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin

from cities_light.models import City, Region



class AboutAdmin(ImportExportModelAdmin):
     model= About
     filter_horizontal = ('images',) #If you don't specify this, you will get a multiple select widget.


class StoreAdmin(admin.ModelAdmin):
    search_fields = ['city__name', 'business_name']
    autocomplete_fields = ['city']
    list_display = ('business_name', 'merchant', 'ref_code')


class LocationAdmin(admin.ModelAdmin):
    search_fields = ['city__name', 'state__name', 'user__username']
    autocomplete_fields = ['city', 'state']

class TestimonialAdmin(admin.ModelAdmin):
    list_display            = ('author', 'store', 'rating')
    list_filter             = ('created_at', 'updated_at')     
    search_fields           = ('author', 'store')
    date_hierarchy          = ('created_at')


admin.site.register(Store, StoreAdmin)
admin.site.register(Offer)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Address, LocationAdmin)
admin.site.register(Promotion)
admin.site.register(Images)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(About, AboutAdmin)
