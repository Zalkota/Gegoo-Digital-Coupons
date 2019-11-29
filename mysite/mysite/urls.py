from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from .views import (
    home,
    ContactFormView,
    contactLandingPage,
    components,
)
from search import views as search_views

#Rerouting django admin through allauth
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from allauth.account import views as allauthviews

#Stemletic App Models
from .views import security

admin.site.login = staff_member_required(login_url='/', redirect_field_name='')(admin.site.login)
#wagtailadmin_urls = staff_member_required(login_url='/', redirect_field_name='')(wagtailadmin_urls)

# redirect_to_my_auth(request):
    #return redirect_to_login(reverse('wagtailadmin_home'), login_url='accounts:login')

urlpatterns = [

    #Security
    path('.well-known/security.txt', security, name='security'),
    #Authentication
    url(r'^accounts/', include('allauth.urls')),
    #Portal
    #url(r'^portal/', include(('portal.urls', 'portal'), namespace='portal')),
    #shoppingcart
    url(r'^cart/', include(('shoppingcart.urls', 'shoppingcart'), namespace='cart')),
    #users
    url(r'', include(('users.urls', 'users'), namespace='users')),

    path('', home, name='home-page'),

    path('components/', components, name='components-page'),

    path('contact/', ContactFormView.as_view(), name='contact-page'),
    path('about/', ContactFormView.as_view(), name='about-page'),
    path('thank-you/', contactLandingPage, name='contact-landing-page'),
    #path('<slug>/', PageDetailView.as_view(), name='page-detail'),
    path('pages', include('django.contrib.flatpages.urls')),

    #Search
    #path('search', search_views.search, name='search'),
    url(r'^search/autocomplete/$', search_views.autocomplete),
    url(r'^find/', search_views.FacetedSearchView.as_view(), name='haystack_search'),

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
