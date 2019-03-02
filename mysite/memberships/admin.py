from django.contrib import admin
from django.contrib.auth.decorators import login_required
# Register your models here.
from .models import Membership, UserMembership, Subscription, Transaction, Benefit, Invoice

#Requires user to login before going to admin site
admin.site.logon = login_required(admin.site.login)

admin.site.register(Membership)
admin.site.register(UserMembership)
admin.site.register(Subscription)
admin.site.register(Transaction)
admin.site.register(Benefit)
admin.site.register(Invoice)
