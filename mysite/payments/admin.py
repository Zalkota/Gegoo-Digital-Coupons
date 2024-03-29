from django.contrib import admin
from payments import models as payments_models
# Register your models here.

class BenefitInline(admin.TabularInline):
    model = payments_models.Plan.benefit.through

class PlanAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'plan_id', 'amount')
    inlines = [
            BenefitInline,
        ]

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscription_id', 'subscription_status', 'payment_status')

admin.site.register(payments_models.Plan, PlanAdmin)
admin.site.register(payments_models.Subscription, SubscriptionAdmin)
admin.site.register(payments_models.Benefit)
admin.site.register(payments_models.Promotion)
admin.site.register(payments_models.PromoUser)
