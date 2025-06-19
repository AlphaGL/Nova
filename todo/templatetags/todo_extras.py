from django import template
register = template.Library()

@register.filter
def get(dictionary, key):
    return dictionary.get(key, {})


@register.filter
def dict_get(d, key):
    """Return d.get(key) or None if missing."""
    if isinstance(d, dict):
        return d.get(key)
    return None