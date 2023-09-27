from django import template
from images.models import *

register = template.Library()

@register.simple_tag()
def get_menu():
    return Menu.objects.all()


