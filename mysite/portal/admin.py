from django.contrib import admin
from .models import Course, Lesson, Review


# Define the admin class
#@admin.register(Product)
#class ProductAdmin(admin.ModelAdmin):
#    pass


admin.site.register(Course)
admin.site.register(Lesson)

admin.site.register(Review)
