def SiteName(request):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    site_name = 'MOD Technologies'
    return {'SITE_NAME': site_name}
