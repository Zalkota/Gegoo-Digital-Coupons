from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Merchant, Offer, Address, Promotion, Images, Category, Subcategory, Tag, About, Favorite
# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin
from leaflet.admin import LeafletGeoAdmin




class AboutAdmin(ImportExportModelAdmin):
     model= About
     filter_horizontal = ('images',) #If you don't specify this, you will get a multiple select widget.


class MerchantAdmin(LeafletGeoAdmin):
    #pass
    list_display = ('business_name', 'category')

admin.site.register(Merchant, MerchantAdmin)

admin.site.register(Offer)
admin.site.register(Address)
admin.site.register(Promotion)
admin.site.register(Images)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Tag)
admin.site.register(About, AboutAdmin)
admin.site.register(Favorite)
