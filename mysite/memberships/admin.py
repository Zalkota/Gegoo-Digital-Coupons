from django.contrib import admin
from django.contrib.auth.decorators import login_required
# Register your models here.
from .models import Membership, UserMembership, Subscription, Transaction, Benefit

#Requires user to login before going to admin site
admin.site.logon = login_required(admin.site.login)


class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ('user', 'timestamp', 'id')

class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ['user_membership', 'stripe_subscription_id']
    list_display = ('user', 'user_membership', 'active', 'stripe_subscription_id')


admin.site.register(Membership)
admin.site.register(UserMembership)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Benefit)
