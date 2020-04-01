from django.urls import path

from payments import views as payments_views
from payments import views_webhooks as payments_views_webhooks

urlpatterns = [
    path('plans/', payments_views.PlanListView.as_view(), name='plan_list'),
    path('plan/<slug:slug>/', payments_views.PlanDetailView.as_view(), name='plan_detail'),

    path('subscription/<slug:slug>', payments_views.SubscriptionDetailView.as_view(), name='subscription_detail'),
    path('subscription/<slug:slug>/manage', payments_views.SubscriptionManageView.as_view(), name='subscription_manage'),

    path('manage-payment-method', payments_views.PaymentMethodManageView.as_view(), name='payment_method_manage'),

    path('webhook/', payments_views_webhooks.TrialWebhook.as_view(), name='webhook'),

    path('charge/', payments_views.Charge.as_view(), name='charge'),

    path('apply-promo', payments_views.ApplyPromo, name='apply_promo')
]
