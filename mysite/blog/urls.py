from django.urls import path, include
from .views import (
    contactLandingPage,
    ContactFormView,
)
from blog import views as blog_views

urlpatterns = [
    path('frequently_asked_questions', blog_views.QuestionListView.as_view(), name='questions_list'),
    path('<slug:slug>/', blog_views.QuestionDetailView.as_view(), name='questions_detail'),
    path('topics/<slug:slug>', blog_views.TopicDetailView.as_view(), name='topics_detail'),
    # path('create/', blog_views.QuestionCreateView.as_view(), name='questions_create'),
    # path('questions/<slug:slug>/update', blog_views.QuestionUpdateView.as_view(), name='questions_update'),
    # path('questions/<slug:slug>/delete', blog_views.QuestionDeleteView.as_view(), name='questions_delete'),
    path('contact/', ContactFormView.as_view(), name='contact-page'),
    path('about/', ContactFormView.as_view(), name='about-page'),
    path('thank-you/', contactLandingPage, name='contact-landing-page'),
]
