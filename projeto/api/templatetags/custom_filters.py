from django import template

register = template.Library()

@register.filter
def get_field(obj, field):
    """
    Retorna o valor do campo especificado do objeto fornecido.
    """
    return getattr(obj, field, None)
