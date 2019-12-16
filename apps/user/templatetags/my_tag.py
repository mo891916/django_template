from django import template

register = template.Library()

 
@register.filter
def find(value, arg):
    try:
        value.index(arg)
        return True
    except:
        return False
