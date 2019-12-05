from django import template

register = template.Library()

@register.filter
def dividebyth(value):
    print(type(value))
    value = round(value, 2)
    return value
