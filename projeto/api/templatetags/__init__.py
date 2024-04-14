from django.template import Library
from .custom_filters import get_field

register = Library()

# Registro das tags personalizadas
register.filter('get_field', get_field)