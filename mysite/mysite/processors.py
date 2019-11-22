from shoppingcart.models import Promotion

def SiteName(request):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    site_name = 'BravePrinting'
    return {'SITE_NAME': site_name}


def PromotionProcessor(request):
    try:
        promotion_qs = Promotion.objects.filter(active=True)
        if promotion_qs.exists():
            promotion = promotion_qs.first()
            message = promotion.message
            background = promotion.background

            context = {
            'message': message,
            'background': background,
            }
            return context
    except:
        return None
