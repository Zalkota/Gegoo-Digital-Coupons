from django.contrib import admin
from payments import models as payments_models
# Register your models here.

class BenefitInline(admin.TabularInline):
    model = payments_models.Plan.benefit.through

class PlanAdmin(admin.ModelAdmin):
    exclude = ('benefit',)
    inlines = [
            BenefitInline,
        ]

admin.site.register(payments_models.Plan, PlanAdmin)
admin.site.register(payments_models.Subscription)
admin.site.register(payments_models.Benefit)
