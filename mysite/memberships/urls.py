from django.urls import path

from .views import (
	MembershipSelectView,
	PaymentView,
	success,
	updateTransactionRecords,
	cancelSubscription,
	cancelSubscriptionAdmin,
	permission_denied,
	)

app_name = 'memberships'

urlpatterns = [

    path('', MembershipSelectView.as_view(), name='select'),
    path('checkout/', PaymentView, name='payment'),
	path('success/<selected_membership>/', success, name='purchase_success'),
    path('update-transactions/<subscription_id>/', updateTransactionRecords, name='update_transactions'),
    path('cancel/<subscription_id>', cancelSubscription, name='cancel'),
	path('cancelAdmin/<stripe_subscription_id>/<user>/', cancelSubscriptionAdmin, name='cancelAdmin'),
	path('permission_denied/', permission_denied, name='permission_denied'),
]
