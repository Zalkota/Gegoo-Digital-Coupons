from portal.models import Promotion, Address
from django.shortcuts import get_list_or_404, get_object_or_404

def SiteName(request):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    site_name = 'Gegoo'
    return {'SITE_NAME': site_name}


def PromotionProcessor(request):
    promotion_qs = Promotion.objects.filter(active=True)
    if promotion_qs.exists():
        promotion = promotion_qs.first()
        message = promotion.message
        background = promotion.background
        promotionActive = True
        context = {
        'message': message,
        'background': background,
        'promotionActive': promotionActive,
        }
    else:
        promotionActive = False
        context = {
        'promotionActive': promotionActive,
        }
    return context


def AuthenticatedUserLocation(request):
    if request.user.is_authenticated:
        #use get instead of filter when querying only one object
        user = request.user
        city = user.user_profile.address.city
        state = user.user_profile.address.state

        context = {
        'city': city,
        'state': state
        }
        return context
    else:
        return context

def classloudFrontURL(request):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    CloudFrontURL = 'https://d7ge9247f1u94.cloudfront.net/'
    return {'CloudFrontURL': CloudFrontURL}
