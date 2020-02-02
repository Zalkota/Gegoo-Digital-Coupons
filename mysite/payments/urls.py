from django.urls import path

from payments import views as payments_views
from payments import webhooks as payments_webhooks

urlpatterns = [
    path('plans/', payments_views.PlanListView.as_view(), name='plan_list'),
    path('plan/<slug:slug>/', payments_views.PlanDetailView.as_view(), name='plan_detail'),

    path('subscription/<slug:slug>', payments_views.SubscriptionDetailView.as_view(), name='subscription_detail'),
    path('payment-intent/', payments_views.PaymentIntent.as_view(), name='payment_intent'),

    path('webhook/', payments_webhooks.TrialWebhook.as_view(), name='webhook'),

    path('charge/', payments_views.Charge.as_view(), name='charge'),
]