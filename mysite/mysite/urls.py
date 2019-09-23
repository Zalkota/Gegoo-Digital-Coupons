from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin

#Rerouting django admin through allauth
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from allauth.account import views as allauthviews

#Stemletic App Models
from .views import security
from users.views import  UserDetailView, UserRedirectView, UserUpdateView, RedirectProfileView, userPage, add_image, user_jobs_view

admin.site.login = staff_member_required(login_url='/', redirect_field_name='')(admin.site.login)
#wagtailadmin_urls = staff_member_required(login_url='/', redirect_field_name='')(wagtailadmin_urls)

# redirect_to_my_auth(request):
    #return redirect_to_login(reverse('wagtailadmin_home'), login_url='accounts:login')

urlpatterns = [

    #Security
    path('.well-known/security.txt', security, name='security'),

    #Authentication
    url(r'^accounts/', include('allauth.urls')),

    #home
    path('', include('home.urls')),

    #Portal
    url(r'^portal/', include(('portal.urls', 'portal'), namespace='portal')),

    #Users
    url(r'^profile/$', userPage, name='userPage'),
    url(r'^users/~redirect/$', UserRedirectView.as_view(), name='redirect'),
    url(r'^users/(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^users/~update/$', UserUpdateView.as_view(), name='update'),
    url(r'^users/redirectprofile/$', RedirectProfileView.as_view(), name='redirectprofile'),
    path('users/update/image/', add_image, name='update_image'),
    path('orders/', user_jobs_view, name='user_jobs'),

    path('admin/', admin.site.urls),


    #Ckeditor
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
