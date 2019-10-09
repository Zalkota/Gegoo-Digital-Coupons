def SiteName(request):
    # Create fixed data structures to pass to template
    # data could equally come from database queries
    # web services or social APIs
    site_name = 'Robert James'
    return {'SITE_NAME': site_name}
