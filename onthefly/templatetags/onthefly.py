import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='jsondumps')
def jsondumps(value):
    if type(value) in [dict, list]:
        return json.dumps(value)
    return value
