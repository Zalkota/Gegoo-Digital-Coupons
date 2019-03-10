from django.urls import path

from .views import (
	MembershipSelectView,
	InvoicePaymentView,
	updateTransactionRecordsInvoice,
	download_invoice_pdf,
	PaymentView,
	success,
	updateTransactionRecords,
	user_subscriptions_view,
	cancelSubscription,
	cancelSubscriptionAdmin,
	refundSubscriptionAdmin,
	TransactionDetailView,
	TransactionListView,
	SubscriptionDetailView,
	SubscriptionListView,
	adminPanel,
	coursePanel,
	lessonPanel,
	MembershipUpdateView,
	MembershipListView,
	permission_denied
	)

app_name = 'memberships'

urlpatterns = [
	# Invoice
	path('invoice-payment/', InvoicePaymentView, name='invoice_payment'),
	path('update-transactions-invoice/<transaction_info>/', updateTransactionRecordsInvoice, name='update_transactions_invoice'),
	path('<invoice_id>/pdf/', download_invoice_pdf, name="invoice_pdf"),

    path('', MembershipSelectView.as_view(), name='select'),
    path('payment/', PaymentView, name='payment'),
	path('success/', success, name='purchase_success'),
    path('update-transactions/<subscription_id>/', updateTransactionRecords, name='update_transactions'),
    path('subscription/', user_subscriptions_view, name='user_subscription'),
    path('cancel/', cancelSubscription, name='cancel'),
	path('cancelAdmin/<stripe_subscription_id>/<user>/', cancelSubscriptionAdmin, name='cancelAdmin'),
	#path('refundAdmin/<user>/', refundSubscriptionAdmin, name='refundAdmin'),

	#TODO MAKE SURE ONLY SUPERUSERS CAN VIEW THESE PAGES
	#Transactions
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('transaction/<uuid:order_id>/', TransactionDetailView.as_view(), name='transaction_detail'),
	#Subscriptions
	path('subscriptions/', SubscriptionListView.as_view(), name='subscription_list'),
	path('subscription/<slug:id>/', SubscriptionDetailView.as_view(), name='subscription_detail'),
	#Admin
    path('admin/', adminPanel, name='admin_panel'),
	#path('admin/courses', coursePanel, name='course_panel'),
	#path('admin/lessons', lessonPanel, name='lesson_panel'),
	path('permission_denied/', permission_denied, name='permission_denied'),
    #Memberships Admin
    path('membership/<int:pk>/update/', MembershipUpdateView.as_view(), name='membership_update'),
	path('memberships/', MembershipListView.as_view(), name='membership_list')
]
