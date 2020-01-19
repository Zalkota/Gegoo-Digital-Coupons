from django.contrib import admin
from payments import models as payments_models
# Register your models here.

admin.site.register(payments_models.Plan)
admin.site.register(payments_models.Subscription)