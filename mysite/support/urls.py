from django.urls import path, include
from .views import (
    contactLandingPage,
    ContactFormView,
    AboutPageView
)
from support import views as support_views

urlpatterns = [
    path('faq/', support_views.QuestionListView.as_view(), name='questions_list'),
    path('faq/<slug:slug>/', support_views.QuestionDetailView.as_view(), name='questions_detail'),
    path('faq/topics/<slug:slug>', support_views.TopicDetailView.as_view(), name='topics_detail'),
    # path('create/', support_views.QuestionCreateView.as_view(), name='questions_create'),
    # path('questions/<slug:slug>/update', support_views.QuestionUpdateView.as_view(), name='questions_update'),
    # path('questions/<slug:slug>/delete', support_views.QuestionDeleteView.as_view(), name='questions_delete'),
    path('contact/', ContactFormView.as_view(), name='contact-page'),
    path('about/', AboutPageView, name='about-page'),
    path('thank-you/', contactLandingPage, name='contact-landing-page'),
]
