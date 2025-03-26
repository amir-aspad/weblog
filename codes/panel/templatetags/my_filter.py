from django import template

register = template.Library()

@register.filter(name='set_default')
def reverse_string(value):
    return value if value else '---'