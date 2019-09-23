from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings

from django.contrib.sitemaps.views import sitemap
from home.sitemaps import StaticViewSitemap, PageSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'post': PageSitemap
}

urlpatterns = [

    path('', views.home, name='home-page'),
    #path('services/', views.ContactFormView.as_view(), name='services-page'),
    #path('products/', views.ProductList, name='products-page'),
    #path('furnaces/', views.FurnaceListView.as_view(), name='furnaces-page'),
    #path('air-conditioning/', views.AirConditioningListView.as_view(), name='air-conditioning-page'),
    #path('deals/', views.deals, name='deals-page'),
    path('contact/', views.ContactFormView.as_view(), name='contact-page'),
    path('about/', views.ContactFormView.as_view(), name='about-page'),
    path('thank-you/', views.contactLandingPage, name='contact-landing-page'),
    #path('<slug>/', PageDetailView.as_view(), name='page-detail'),
    path('pages', include('django.contrib.flatpages.urls')),


    #Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
