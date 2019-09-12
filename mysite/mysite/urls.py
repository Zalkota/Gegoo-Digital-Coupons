from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin

#Rerouting django admin through allauth
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from allauth.account import views as allauthviews

#Wagtail
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from search import views as search_views

#Stemletic App Models
from .views import security
from portal.views import SubscriptionListView, CourseListView, CourseDetailView, LessonDetailView, SearchTitles #ProductDetailView, ProductCreateView, ProductUpdateView,
from users.views import  UserDetailView, UserRedirectView, UserUpdateView, RedirectProfileView, userPage, add_image, user_subscriptions_view
from memberships.views import get_user_membership, get_user_subscription, get_selected_membership, MembershipSelectView, PaymentView, updateTransactionRecords, cancelSubscription

admin.site.login = staff_member_required(login_url='/', redirect_field_name='')(admin.site.login)
#wagtailadmin_urls = staff_member_required(login_url='/', redirect_field_name='')(wagtailadmin_urls)

# redirect_to_my_auth(request):
    #return redirect_to_login(reverse('wagtailadmin_home'), login_url='accounts:login')

urlpatterns = [

    #Security
    path('.well-known/security.txt', security, name='security'),

    #Generic
    url(r'^django-admin/', admin.site.urls),

    #url(r'^cms/login', redirect_to_my_auth, name='wagtailadmin_urls'),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    # Wagtail Search
    #url(r'^search/$', search_views.search, name='search'),

    #Authentication
    url(r'^accounts/', include('allauth.urls')),

    #Product
    url(r'^portal/', include(('portal.urls', 'portal'), namespace='portal')),

    #Membership
    url(r'^membership/', include(('memberships.urls', 'memberships'), namespace='memberships')),

    #Users
    url(r'^profile/$', userPage, name='userPage'),
    url(r'^users/~redirect/$', UserRedirectView.as_view(), name='redirect'),
    url(r'^users/(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^users/~update/$', UserUpdateView.as_view(), name='update'),
    url(r'^users/redirectprofile/$', RedirectProfileView.as_view(), name='redirectprofile'),
    path('users/update/image/', add_image, name='update_image'),
    path('subscription/', user_subscriptions_view, name='user_subscription'),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
