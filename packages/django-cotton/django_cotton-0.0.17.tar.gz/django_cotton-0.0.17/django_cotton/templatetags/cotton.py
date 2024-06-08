from django import template
from django.utils.html import format_html_join

from django_cotton.templatetags._component import cotton_component
from django_cotton.templatetags._slot import cotton_slot
from django_cotton.templatetags._props import cotton_props
from django_cotton.templatetags._props_frame import cotton_props_frame

register = template.Library()
register.tag("cotton_component", cotton_component)
register.tag("cotton_slot", cotton_slot)
register.tag("cotton_props", cotton_props)
register.tag("cotton_props_frame", cotton_props_frame)


@register.filter
def merge(attrs, args):
    # attrs is expected to be a dictionary of existing attributes
    # args is a string of additional attributes to merge, e.g., "class:extra-class"
    for arg in args.split(","):
        key, value = arg.split(":", 1)
        if key in attrs:
            attrs[key] = value + " " + attrs[key]
        else:
            attrs[key] = value
    return format_html_join(" ", '{0}="{1}"', attrs.items())
