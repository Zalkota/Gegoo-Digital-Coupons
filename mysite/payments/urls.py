from django.urls import path

from payments import views as payments_views

urlpatterns = [
    path('plans/', payments_views.PlanListView.as_view(), name='plan_list'),
    path('plan/<slug:slug>/', payments_views.PlanDetailView.as_view(), name='plan_detail'),
    path('charge/', payments_views.Charge.as_view(), name='charge'),
]