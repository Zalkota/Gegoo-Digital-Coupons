from django.views.generic.base import TemplateView
from files.views import FilePolicyAPI, FileUploadCompleteHandler, VideoFileUploadView
from django.urls import path


urlpatterns = [

    path('upload/', TemplateView.as_view(template_name='files/upload.html'), name='upload-home'),
    path('api/files/policy/', FilePolicyAPI.as_view(), name='upload-policy'),
    path('api/files/complete/', FileUploadCompleteHandler.as_view(), name='upload-complete'),

    # path('video-upload/store/<slug:slug>/', VideoFileUploadView.as_view(), name='merchant_video_upload'),







]
