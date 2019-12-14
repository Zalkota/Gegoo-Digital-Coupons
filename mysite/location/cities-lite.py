# An example is worth 1000 words: if you want to import only cities from France, USA and Belgium you could
# do as such:

# import cities_light
#
# def filter_city_import(sender, items, **kwargs):
# if items[8] not in ('FR', 'US', 'BE'):
# raise cities_light.InvalidItems()
# cities_light.signals.city_items_pre_import.connect(filter_city_import)
