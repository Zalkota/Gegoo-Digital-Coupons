from django.conf import settings

from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from .views import (
    homeView,
    AltHomeView,
)
from .views import set_location_cookies
from search import views as search_views
#sitemaps
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages.sitemaps import FlatPageSitemap
#Rerouting django admin through allauth
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from allauth.account import views as allauthviews

#Stemletic App Models
from .views import security

admin.site.login = staff_member_required(login_url='/', redirect_field_name='')(admin.site.login)

from .sitemaps import StaticSitemap, SupportSitemap, QuestionSitemap, TopicSitemap, StoreSitemap

sitemaps = {
    'mysite': StaticSitemap,
    'support': SupportSitemap,
    'question': QuestionSitemap,
    'topic': TopicSitemap,
    'store': StoreSitemap,
}

urlpatterns = [

    #Admin
    path('admin/', admin.site.urls),
    #SiteMap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    #path('alt-home/', AltHomeView.as_view(), name='alt-home'),
    path('', homeView.as_view(), name='home-page'),
    #Security
    path('.well-known/security.txt', security, name='security'),
    #Authentication
    url(r'^accounts/', include('allauth.urls')),
    #Portal
    url(r'^shop/', include(('portal.urls', 'portal'), namespace='portal')),
    #Location
    url(r'^', include(('location.urls', 'location'), namespace='location')),
    #Portal
    path('payments/', include(('payments.urls', 'payments'), namespace='payments')),
    #FAQ
    url(r'^support/', include(('support.urls', 'support'), namespace='support')),
    #users
    url(r'', include(('users.urls', 'users'), namespace='users')),
    #files
    url(r'^', include(('files.urls', 'files'), namespace='files')),
    #FlatPages
    path('pages', include('django.contrib.flatpages.urls')),
    #Search
    #path('search', search_views.search, name='search'),
    url(r'^search/autocomplete/$', search_views.autocomplete),
    url(r'^find/', search_views.FacetedSearchView.as_view(), name='haystack_search'),
    #Ckeditor
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),


    path('sitemap.xml', sitemap,
        {'sitemaps': {'flatpages': FlatPageSitemap}},
        name='django.contrib.sitemaps.views.sitemap'),


    #Development
    # path('components/', components, name='components-page'),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
