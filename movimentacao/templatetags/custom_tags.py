from django import template

register = template.Library()

@register.simple_tag
def subtract(value1, value2):
    return value1 - value2