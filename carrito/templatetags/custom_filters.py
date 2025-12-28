from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica value * arg y retorna el resultado."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
