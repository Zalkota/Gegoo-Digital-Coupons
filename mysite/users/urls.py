from django.conf.urls import url
from django.urls import path
from users import views as users_views
from users import views_approval as users_approval_views
from users import views_admin as users_admin_views
from portal import views as portal_views
from files import views as files_views

urlpatterns = [

    path('dashboard/', users_views.userPage.as_view(), name='userPage'),
    path('admin/dashboard', users_admin_views.AdminDashboardView.as_view(), name='admin_dashboard'),

    # Admin Dashboard
    path('admin/approve-users', users_admin_views.AdminApproveUsersView.as_view(), name='admin_approve_users'),
    path('admin/manage-subscriptions', users_admin_views.AdminManageSubscriptionsView.as_view(), name='admin_manage_subscriptions'),

    #Consumer User Profile
    path('dashboard/location/', users_views.userLocaton.as_view(), name='user_location'),
    path('dashboard/rewards/', users_views.userRewards.as_view(), name='user_rewards'),
    path('dashboard/favorite-offers/', users_views.userFavorites.as_view(), name='user_favorites'),
    path('dashboard/merchant-offers/', users_views.userFavorites.as_view(), name='user_merchants'),
    url(r'^users/~redirect/$', users_views.UserRedirectView.as_view(), name='redirect'),
    url(r'^users/~update/$', users_views.UserUpdateView.as_view(), name='user_profile_update'),
    url(r'^users/redirectprofile/$', users_views.RedirectProfileView.as_view(), name='redirectprofile'),

    #Merchant
    # path('my-subscription/', users_views.MerchantSubscriptionsView.as_view(), name='subscription_list'),

    # Merchant Store Views
    path('my-store/<slug:slug>/', portal_views.MerchantStoreDetailView.as_view(), name='merchant_store_detail'),
    path('my-stores/', portal_views.MerchantStoreListView.as_view(), name='merchant_store_list'),
    # path('my-store/create/', portal_views.MerchantStoreCreateView.as_view(), name='merchant_store_create'), #REMOVED
    path('my-store/<slug:slug>/update/', portal_views.MerchantStoreUpdateView.as_view(), name='merchant_store_update'),
    path('my-store/<slug:slug>/delete/', portal_views.MerchantStoreDeleteView.as_view(), name='merchant_store_delete'),


    #Merchant Offer Views
    path('my-offers/', portal_views.MerchantOfferListView.as_view(), name='merchant_offer_list'),
    path('my-offers/create/', portal_views.MerchantOfferCreateView.as_view(), name='merchant_offer_create'),
    path('my-offer/<slug:slug>/', portal_views.MerchantOfferDetailView.as_view(), name='merchant_offer_detail'),
    path('my-offer/<slug:slug>/update/', portal_views.MerchantOfferUpdateView.as_view(), name='merchant_offer_update'),
    path('my-offer/<slug:slug>/delete/', portal_views.MerchantOfferDeleteView.as_view(), name='merchant_offer_delete'),
    path('my-offer/like/', portal_views.OfferLike, name='offer_like'),

    #Merchant Signup Forms
    path('merchant-signup/', users_views.MerchantSignUpView.as_view(), name='merchant-signup'),

    #Merchant Approval Views
    path('approval/store/create/', users_approval_views.MerchantApprovalStoreCreateView.as_view(), name='merchant_approval_store_create'),
    path('approval/store/create/additional/',  users_approval_views.MerchantApprovalAdditionalStoreView.as_view(), name='merchant_approval_additional_store'),
    path('approval/store/upload/content/<slug:slug>/', files_views.MerchantContentDetailView.as_view(), name='merchant_content_detait'),
    path('approval/store/upload/file-type/<slug:slug>/', files_views.FileUploadSelector.as_view(), name='merchant_approval_file_select'),
    path('approval/store/upload/image/<slug:slug>/', files_views.ImageFileUploadView.as_view(), name='merchant_approval_image_upload'),
    path('approval/store/upload/video/<slug:slug>/', files_views.VideoFileUploadView.as_view(), name='merchant_approval_video_upload'),
    path('approval/store/upload/file/<slug:slug>/', files_views.FileUploadView.as_view(), name='merchant_approval_file_upload'),

    #Video
    path('my-video/<slug:slug>/delete', files_views.MerchantVideoFileDeleteView.as_view(), name='merchant_video_delete'),
    path('my-video/<slug:slug>/', files_views.MerchantVideoFileDetailView.as_view(), name='merchant_video_detail'),

    #Images
    path('my-images/<slug:slug>/delete', files_views.MerchantImageFileDeleteView.as_view(), name='merchant_image_delete'),
    path('my-images/<slug:slug>/', files_views.MerchantImageFileDetailView.as_view(), name='merchant_image_detail'),

    #Downloadable Content
    path('my-files/<slug:slug>/delete', files_views.MerchantFileDeleteView.as_view(), name='merchant_file_delete'),
    path('my-files/<slug:slug>/', files_views.MerchantFileDetailView.as_view(), name='merchant_file_detail'),

    #Merchant Testimonials
    path('my-reviews/', portal_views.MerchantTestimonialListView.as_view(), name='merchant_testimonial_list'),
    path('new-review/<slug:slug>/', portal_views.MerchantTestimonialCreateView.as_view(), name='merchant_testimonial_create'),

    #Connections
    path('connect/<str:operator>/<int:pk>', users_views.ChangeConnections, name='change_connections'),


]
