from django import template

register = template.Library()

@register.filter()
def get_value(arr, key):
    return arr[int(key)]
