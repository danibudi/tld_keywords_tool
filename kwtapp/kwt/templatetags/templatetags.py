#templatetags.py
from django import template
from django.template.defaultfilters import stringfilter
from models import Keyword, Kw_sv_language

register = template.Library()

@register.filter
@stringfilter
def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

