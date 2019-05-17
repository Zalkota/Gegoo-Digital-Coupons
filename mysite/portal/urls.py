from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path
from . import views
#from .views import ProductDetailView
from .views import AppointmentFormView

#NOTE: https://github.com/codingforentrepreneurs/Guides/blob/master/all/common_url_regex.md

urlpatterns = [

    url(r'^subscriptions/$', views.SubscriptionListView, name='subscription_list'),
    path('consultation/', views.AppointmentFormView, name='appintment_form'),
    #url(r'^courselist/$', CourseListView, name='course_list'),
    #path('contact/<email>/<user>/', views.Contact, name='contact_form'),
    #path('<slug>', CourseDetailView.as_view(), name='course_detail'),
    #path('<course_slug>/<lesson_slug>', views.LessonDetailView, name='lesson_detail'),
    # Courses
    #path('course/create/', views.CourseCreateView.as_view(), name='course_create'),
    #path('course/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    #path('course/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    # Lessons
    #path('lesson/create/', views.LessonCreateView.as_view(), name='lesson_create'),
    #path('lesson/<int:pk>/update/', views.LessonUpdateView.as_view(), name='lesson_update'),
    #path('lesson/<int:pk>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),
    #path('next-lesson/<course_slug>/<lesson_slug>', next_lesson, name='next_lesson'),
    #path('previous-lesson/<course_slug>/<lesson_slug>', previous_lesson, name='previous_lesson'),
    #path('membership_required/', membership_required, name='membership_required'),
    # Reviews
    #path('review/<course>/new/', views.Review, name='review_form'),
    # Search function
    #path('courselist/search/', SearchTitles, name='search_titles'),

]
