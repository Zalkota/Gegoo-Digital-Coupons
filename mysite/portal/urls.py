from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path
from . import views
from .views import JobCreateView, ImageUploadView, HowItWorks, JobPaymentView, success, updateTransactionRecordsJob


#NOTE: https://github.com/codingforentrepreneurs/Guides/blob/master/all/common_url_regex.md

urlpatterns = [

    path('image-upload/', ImageUploadView.as_view(), name='image_upload'),
    path('how-it-works/', views.HowItWorks, name='how_it_works'),
    path('job-request/', views.JobCreateView, name='job_request'),

    #url(r'^subscriptions/$', views.SubscriptionListView, name='subscription_list'),
    #path('consultation/', views.AppointmentFormView, name='appintment_form'),

    #Payment
    path('checkout/', JobPaymentView, name='job_payment'),
	path('success/', success, name='purchase_success'),
    path('update-transactions/<transaction_info>/', updateTransactionRecordsJob, name='update_transaction_job'),
]
