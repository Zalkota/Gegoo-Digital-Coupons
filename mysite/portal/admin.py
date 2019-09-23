from django.contrib import admin
from .models import Job, Review, Image
from django.contrib.auth.decorators import login_required

# Define the admin class
#@admin.register(Product)
#class ProductAdmin(admin.ModelAdmin):
#    pass

#Requires user to login before going to admin site
admin.site.logon = login_required(admin.site.login)

admin.site.register(Job)
admin.site.register(Image)
admin.site.register(Review)
