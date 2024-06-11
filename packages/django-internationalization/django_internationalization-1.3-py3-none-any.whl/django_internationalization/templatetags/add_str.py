from django import template

register = template.Library()

@register.filter
def add_str(str1, str2):
    return str(str1) + str(str2)