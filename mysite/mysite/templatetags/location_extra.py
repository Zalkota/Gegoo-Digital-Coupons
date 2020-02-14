from django import template

register = template.Library()

@register.filter
def dividebyth(value):
    value = round(value, 1)
    return value

@register.filter
def ratingsystem(value):
    value = round(value, 1)
    rating = []
    for i in value:
        rating.append('star')

    negative_value = 5 - value

    for i in negative_value:
        rating.append('star_border')
    print(rating)
    return rating
